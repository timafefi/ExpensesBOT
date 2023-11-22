from db import db
from aiogram import types, Router, F, Bot
from aiogram.fsm.context import FSMContext
from keyboards import category_inline
from aiogram.filters.command import Command
import functions
from functions import OpState
from states import State
import text



router = Router()

@router.message(Command('start'))
async def cmd_start(message: types.Message, state: FSMContext):
    if not db.update_user(message.from_user):
        return
    await state.set_state(State.start)
    await message.answer(text.hello_msg, parse_mode='html')


@router.message(State.start, F.text)
async def cmd_report(message: types.Message, state: FSMContext):
    split = message.text.split(' ')

    if functions.get_operation(split) == OpState.spending:
        await state.update_data(_type=1)
        try:
            await state.update_data(amount=abs(float(split[0])))
            if len(split) > 1:
                await state.update_data(msg=' '.join(split[1:]))
        except ValueError:
            await state.update_data(amount=abs(float(split[1])))
            if len(split) > 2:
                await state.update_data(msg=' '.join(split[2:]))
        await message.answer("Выберите категорию", reply_markup=category_inline.cat_fab())
        await state.set_state(State.register)

    elif functions.get_operation(split) == OpState.earning:
        data = {'userid': message.from_user.id, '_type': 0}
        try:
            data['amount'] = abs(float(split[0]))
            if len(split) > 1:
                data['msg'] = ' '.join(split[1:])
        except ValueError:
            data['amount'] = abs(float(split[1]))
            if len(split) > 2:
                data['msg'] = ' '.join(split[2:])
        db.register(data)
        await message.answer(text.done_msg)

    elif functions.get_operation(split) == OpState.zero:
        await message.answer("Не выебывайся")

    else:
        await message.answer("Неправильный ввод. Формат: +150 чаевые")



@router.callback_query(State.register, 
        category_inline.CatCallFac.filter())
async def write_to_db(
        callback: types.CallbackQuery,
        callback_data: category_inline.CatCallFac,
        state: FSMContext):
    data = await state.get_data()
    data['category'] = callback_data.index
    data['userid'] = callback.from_user.id
    db.register(data)
    await callback.message.edit_text(text=text.done_msg,  reply_markup=None)
    await state.set_state(State.start)
    

