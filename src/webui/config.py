from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "ECommerce"
    app_version: str = "1.0.0"
    base_url: str = "/api/v1/"

    class Config:
        env_file = ".env"


settings = Settings()
