from aiogram.fsm.state import StatesGroup, State

class State(StatesGroup):
    register = State()
    start = State()
    info = State()

