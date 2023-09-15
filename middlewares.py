from aiogram import types
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware
import logging
from datetime import datetime
from db import db

class AccessMiddleware(BaseMiddleware):
    def __init__(self, access_usernames):
        self.access_usernames = access_usernames
        super.__init__()

    async def __call__(self, handler, event, data)



