from db import db
from aiogram import types, Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.filters.command import Command
from states import State
import functions
from keyboards.pageskb import Pages, PagesFact

router = Router()
pages = Pages(10)

@router.message(Command('stats'))
async def cmd_stats(message: types.Message, state: FSMContext):
    data = db.get_info(offset=0, limit=pages.lines,from_date=functions.cm_stamp())
    maxlines = db.count_all_expences()
    stats = functions.print_stats(data)
    print(pages.generate(maxlines, offset=0))
    await message.answer(stats, parse_mode='html',
                         reply_markup=pages.generate(maxlines, offset=0))


@router.callback_query(PagesFact.filter())
async def move_pages(callback: types.CallbackQuery, callback_data: PagesFact):
    print("ji")
    if callback_data.action == 'left':
        new_offset = callback_data.offset-pages.lines
    elif callback_data.action == 'right':
        new_offset = callback_data.offset+pages.lines
    else:
        return
    data = db.get_info(offset=new_offset, limit=pages.lines,from_date=functions.cm_stamp())
    maxlines = db.count_all_expences()
    stats = functions.print_stats(data)
    await callback.message.edit_text(stats, parse_mode='html',
                         reply_markup=pages.generate(maxlines, new_offset))

