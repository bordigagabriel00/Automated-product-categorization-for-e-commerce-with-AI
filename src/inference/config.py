from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Inference"
    app_version: str = "1.0.0"
    description: str = "Automated product categorization for e-commerce with AI"
    base_url: str = "/api/v1/"
    nats_url: str = "nats://127.0.0.1:4222"

    class Config:
        env_file = ".env"


settings = Settings()
