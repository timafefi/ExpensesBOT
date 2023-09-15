from pydantic_settings import BaseSettings
from pydantic import SecretStr

class Settings(BaseSettings):
    bot_token: SecretStr
    users: tuple = [
        {'username': 'timafefi', 'admin': True},
        {'username': 'darystroganova', 'admin': False}

    ]
    categories: tuple = ['Продукты', 'Фастфуд/Рестораны',
        'Различные товары', 'Связь/Подписки', 'Транспорт', 'Аренда']

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


config = Settings()

