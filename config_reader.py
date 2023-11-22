from pydantic_settings import BaseSettings
from pydantic import SecretStr
from text import Emoji

class Settings(BaseSettings):
    bot_token: SecretStr
    users: tuple = [
        {'username': 'timafefi', 'admin': True},
        {'username': 'darystroganova', 'admin': False}

    ]
    categories: tuple = [
        f'Продукты{Emoji.food}',                  #0
        f'Рестораны {Emoji.cafe}',                #1
        f'Разное{Emoji.other}',                   #2 
        f'Подписки{Emoji.subscriptions}',         #3
        f'Транспорт{Emoji.transport}',            #4
        f'Аренда{Emoji.rent}'                     #5
    ]

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


config = Settings()

