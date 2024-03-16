
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    nats_url: str = "nats://localhost:4222"
    arango_url: str = "http://localhost:8529"
    name_system_db: str = "_system"
    username: str = "root"
    password: str = "rootpassword"
    csv_file: str = "products.csv"
    product_url: str = "https://raw.githubusercontent.com/anyoneai/e-commerce-open-data-set/master/products.json"

    class Config:
        env_file = ".env"


settings = Settings()
