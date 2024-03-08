from dotenv import load_dotenv, find_dotenv
from pydantic_settings import BaseSettings
from os import getenv

load_dotenv(find_dotenv())


class DBSettings(BaseSettings):
    host: str = getenv("HOST")
    port: int = getenv("PORT")
    user: str = getenv("USER")
    password: str = getenv("PASSWORD")
    database_name: str = getenv("DATABASE")


class Settings(DBSettings):
    token: str = getenv("BOT_TOKEN")
    db: DBSettings = DBSettings()


settings = Settings()
