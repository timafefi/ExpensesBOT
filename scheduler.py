from aiogram import Dispatcher
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from db import db



class Scheduler:

    def __init__(self, dp):
        self.scheduler = AsyncIOScheduler()
        self.dp = dp

    async def renew_month_counter(self):
        db.renew_counter()


    def start(self):
        #self.scheduler.add_job(self.send_recurr, "interval", seconds=5)
        self.scheduler.add_job(self.renew_month_counter, "cron", day=1)
        self.scheduler.start()


