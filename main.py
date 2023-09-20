import logging
import asyncio
from aiogram import Bot, Dispatcher
from config_reader import config
from handlers import data_input, info
from aiogram.types import BotCommand, BotCommandScopeDefault

async def set_commands(bot: Bot):
    commands= [
        BotCommand(command='start', description='Запустить'),
        BotCommand(command='stats', description='Показать статистику')
    ]
    await bot.set_my_commands(commands=commands, scope=BotCommandScopeDefault())


logging.basicConfig(level=logging.INFO)
bot = Bot(token=config.bot_token.get_secret_value())
dp = Dispatcher()
dp.include_routers(info.router, data_input.router)


async def main():
    await set_commands(bot)
    await dp.start_polling(bot)




if __name__ == "__main__":
    asyncio.run(main())
