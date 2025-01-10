from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr

class Settings(BaseSettings):
    DB_URL: SecretStr
    SECRET_KEY: SecretStr
    ALGORITHM: SecretStr
    model_config = SettingsConfigDict(
        env_file=".env"
    )
settings = Settings()