from config_reader import config
from typing import Optional
from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder

class CatCallFac(CallbackData, prefix='category'):
    index: int

def cat_fab():
    builder = InlineKeyboardBuilder()
    i = 0
    for cat in config.categories:
        builder.button(text=f'{cat}', callback_data=CatCallFac(index=i))
        i = i + 1
    builder.adjust(1)
    return builder.as_markup()
