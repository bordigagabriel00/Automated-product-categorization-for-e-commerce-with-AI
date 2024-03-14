import logging

import fastapi.applications
import uvicorn
from fastapi import FastAPI

from config import settings
from core import setup
from core.environment import ConfigProvider

# Define the app at the module level
app: fastapi.applications.FastAPI = FastAPI(title=settings.app_name,
                                            description=settings.description,
                                            version=settings.app_version)

environment = ConfigProvider()
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


async def init_options(option: ConfigProvider) -> None:
    option.set_config("app", "title", settings.app_name)
    option.set_config("app", "description", settings.description)
    option.set_config("app", "version", settings.app_version)


def show_api(app: fastapi.FastAPI) -> None:
    routes_list = []
    for route in app.routes:
        if hasattr(route, "methods") and hasattr(route, "path"):
            routes_list.append({"path": route.path, "methods": list(route.methods)})
            logging.info(f"API: '{route}'")


@app.on_event("startup")
async def startup_event():
    logging.info("start configuration")
    # Define environment
    await init_options(environment)

    # Define View, Routers
    await setup.init(app)

    # Show api definitions
    show_api(app)


if __name__ == "__main__":
    # the port is defined by command
    uvicorn.run("main:app", host="0.0.0.0", reload=True)
