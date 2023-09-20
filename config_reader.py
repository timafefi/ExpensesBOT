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
        f'Продукты{Emoji.food}',
        f'Рестораны {Emoji.cafe}',
        f'Разное{Emoji.other}', 
        f'Подписки{Emoji.subscriptions}',
        f'Транспорт{Emoji.transport}',
        f'Аренда{Emoji.rent}'
    ]

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


config = Settings()

