import logging

import uvicorn
from fastapi import FastAPI

# Local imports
from config import settings
from core import setup
from core.bert_model_provider import init_load_bert_model
from core.environment import ConfigProvider
from core.normalization_provider import init_normalization
from core.logger_provider import logger
from fastapi.logger import logger as fastapi_logger

# Configure logging


# Instantiate the FastAPI application
app: FastAPI = FastAPI(
    title=settings.app_name,
    description=settings.description,
    version=settings.app_version
)

fastapi_logger.handlers = logger.handlers
fastapi_logger.setLevel(logger.level)

# Instantiate the configuration provider
environment = ConfigProvider()


async def init_options(option: ConfigProvider) -> None:
    """
    Initializes application options based on the provided configuration.

    Args:
        option (ConfigProvider): The configuration provider instance.
    """
    option.set_config("app", "title", settings.app_name)
    option.set_config("app", "description", settings.description)
    option.set_config("app", "version", settings.app_version)


def show_api(web_app: FastAPI) -> None:
    """
    Logs the API routes available in the application.

    Args:
        web_app (FastAPI): The FastAPI application instance.
    """
    for route in web_app.routes:
        if hasattr(route, "methods") and hasattr(route, "path"):
            logger.info(f"API Route: {route.path} Methods: {list(route.methods)}")


@app.on_event("startup")
async def startup_event():
    """
    Defines actions to be performed at application startup, including:
    - Setting up environment configurations
    - Initializing application routes and views
    - Logging API routes
    - Initializing NLP components
    """

    logger.info("Starting application setup.")

    # Initialize application options
    await init_options(environment)

    # Initialize application views and routers
    await setup.init(app)

    # Log available API routes
    show_api(app)

    # Initialize NLP components
    await init_normalization()
    logger.info("Application setup completed.")

    # Initialize BERT model
    tokenizer, model = await init_load_bert_model()
    if tokenizer is not None and model is not None:
        logger.info("Tokenizer and model are ready to use")
    else:
        logger.error("Failed to load tokenizer and model")


if __name__ == "__main__":
    # Run the application with Uvicorn, with the ability to reload on code changes.
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)

    """
    TODO: Predict models
    TODO: Docker compose / DockerFIle
    TODO: TestUNI
    TODO: Test integrator
    TODO: Video
    TODO: Server
    """
