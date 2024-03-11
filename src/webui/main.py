import logging
import pathlib

import fastapi.applications
import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from config import settings
from core import setup
from core.environment import ConfigProvider

# Define the app at the module level
app: fastapi.applications.FastAPI = FastAPI(title=settings.app_name,
                                            description=settings.description,
                                            version=settings.app_version)

# Define static section
BASE_STATIC_DIR = pathlib.Path(__file__).parent / 'ui' / 'static'
app.mount("/static", StaticFiles(directory=BASE_STATIC_DIR), name="static")

environment = ConfigProvider()
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


async def init_options(option: ConfigProvider) -> None:
    option.set_config("app", "title", settings.app_name)
    option.set_config("app", "description", settings.description)
    option.set_config("app", "version", settings.app_version)
    option.set_config("app", "base_static_dir", BASE_STATIC_DIR)


def show_api(app: fastapi.FastAPI) -> None:
    routes_list = []
    for route in app.routes:
        if hasattr(route, "methods") and hasattr(route, "path"):
            routes_list.append({"path": route.path, "methods": list(route.methods)})
            logging.info(f"API: '{route}'")


@app.on_event("startup")
async def startup_event():
    # Define environment
    await init_options(environment)
    # Define View, Routers
    await setup.init(app)
    # Show api definitions
    show_api(app)


if __name__ == "__main__":
    # the port is defined by command
    uvicorn.run("main:app", host="0.0.0.0", reload=True)

"""
TODO: topic predict.request
TODO: topic predict.response
TODO: Docu
TODO: Product
TODO: Pipelina
"""
