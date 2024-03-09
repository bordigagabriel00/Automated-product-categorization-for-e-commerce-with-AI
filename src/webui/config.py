import pathlib

from fastapi.templating import Jinja2Templates
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "ECommerce"
    app_version: str = "1.0.0"
    description: str = "Automated product categorization for e-commerce with AI"
    base_url: str = "/api/v1/"
    nats_url: str = "nats://localhost:4222"

    class Config:
        env_file = ".env"


BASE_DIR = pathlib.Path(__file__).parent
BASE_TEMPLATE_DIR = BASE_DIR / 'ui' / 'templates'
templates = Jinja2Templates(directory=BASE_TEMPLATE_DIR)
settings = Settings()
