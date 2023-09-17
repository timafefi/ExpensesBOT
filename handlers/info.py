from db import db
from aiogram import types, Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.filters.command import Command
from states import State
import functions

router = Router()

@router.message(State.start, Command('stats'))
async def cmd_stats(message: types.Message, state: FSMContext):
    data = db.get_info(from_date=functions.curr_month_timestamp())
    message.answer(f"Total earned: {data['earned']}\n Total spent: {data['spent']}")

