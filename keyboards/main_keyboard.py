from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def makeKb():
    kb = [
        [KeyboardButton(text='Заработал')],
        [KeyboardButton(text='Потратил')]
    ]
    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
