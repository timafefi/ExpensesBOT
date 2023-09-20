from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder
import enum


class PagesFact(CallbackData, prefix='pages'):
    action: str
    offset: int


class Pages():
    def __init__(self, lines=10):
        self.lines = lines


    def generate(self, max_lines, offset=0):
        stat = f"{offset//self.lines}/{max_lines//self.lines}"
        builder = InlineKeyboardBuilder()
        if offset // self.lines:
            builder.button(text='<', 
                callback_data=PagesFact(action='left', offset=offset))
        else:
            builder.button(text='_', 
                callback_data=PagesFact(action='idle', offset=offset))
        builder.button(text=stat,
                       callback_data=PagesFact(action='idle', offset=offset))
        if offset + self.lines < max_lines:
            builder.button(text='>',
                           callback_data=PagesFact(action='right', offset=offset))
        else:
            builder.button(text='_',
                           callback_data=PagesFact(action='idle', offset=offset))
        builder.adjust(3)
        return builder.as_markup()

            

