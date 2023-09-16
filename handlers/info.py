from db import db
from aiogram import types, Router, F, Bot
from aiogram.fsm.context import FSMContext
from aiogram.filters.command import Command
from states import State

router = Router()

@router.message(State.start, Command('stats'))
async def cmd_stats(message: types.Message, state: FSMContext):
    pass

