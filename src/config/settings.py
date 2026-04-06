# 환경변수를 안전하게 읽는 역할을 함.

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # .env 파일을 읽어서 설정값으로 사용
    model_config = SettingsConfigDict(
      env_file=".env",
      env_file_encoding="utf-8",
      extra="ignore",
    )

    discord_webhook_url: str = Field(..., alias="DISCORD_WEBHOK_URL")
    app_env: str = Field(default="local", alias="APP_ENV")
    timezone: str = Field(default="Asia/Seoul", alias="TIMEZONE")


settings = Settings()