import pathlib

from fastapi.templating import Jinja2Templates
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "WebUI"
    app_version: str = "1.0.0"
    description: str = "Automated product categorization for e-commerce with AI"
    base_url: str = "/api/v1"
    nats_url: str = "nats://127.0.0.1:4222"
    arango_url: str = "http://127.0.0.1:8529"
    name_system_db: str = "_system"
    product_model_db: str = "Product_Model"
    username: str = "root"
    password: str = "rootpassword"
    csv_file: str = "products.csv"
    product_url: str = "https://raw.githubusercontent.com/anyoneai/e-commerce-open-data-set/master/products.json"

    class Config:
        env_file = ".env"


BASE_DIR = pathlib.Path(__file__).parent
BASE_TEMPLATE_DIR = BASE_DIR / 'ui' / 'templates'
templates = Jinja2Templates(directory=BASE_TEMPLATE_DIR)

settings = Settings()
