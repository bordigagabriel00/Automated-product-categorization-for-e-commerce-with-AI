import logging

import uvicorn
from fastapi import FastAPI

# Local imports
from config import settings
from core import setup
from core.environment import ConfigProvider
from core.normalization_provider import init_normalization

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Instantiate the FastAPI application
app: FastAPI = FastAPI(
    title=settings.app_name,
    description=settings.description,
    version=settings.app_version
)

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
            logging.info(f"API Route: {route.path} Methods: {list(route.methods)}")


@app.on_event("startup")
async def startup_event():
    """
    Defines actions to be performed at application startup, including:
    - Setting up environment configurations
    - Initializing application routes and views
    - Logging API routes
    - Initializing NLP components
    """

    logging.info("Starting application setup.")

    # Initialize application options
    await init_options(environment)

    # Initialize application views and routers
    await setup.init(app)

    # Log available API routes
    show_api(app)

    # Initialize NLP components
    init_normalization()
    logging.info("Application setup completed.")


if __name__ == "__main__":
    # Run the application with Uvicorn, with the ability to reload on code changes.
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
