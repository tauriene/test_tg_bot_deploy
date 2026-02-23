import pathlib
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr


env_path = pathlib.Path(__file__).parent.parent.parent / ".env"


class Settings(BaseSettings):
    bot_token: SecretStr
    ai_text_token: SecretStr
    debug: bool = False

    model_config = SettingsConfigDict(env_file=env_path, env_file_encoding="utf-8")


settings = Settings()
