import logging
import asyncio
from aiogram import Bot, Dispatcher
from config_reader import config
from handlers import data_input, info
from scheduler import Scheduler

logging.basicConfig(level=logging.INFO)
bot = Bot(token=config.bot_token.get_secret_value())
dp = Dispatcher()
dp.include_routers(data_input.router, info.router)
scheduler = Scheduler(dp)


async def main():
    scheduler.start()
    await dp.start_polling(bot)




if __name__ == "__main__":
    asyncio.run(main())
