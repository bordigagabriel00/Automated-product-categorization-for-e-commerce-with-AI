import uvicorn
import pathlib
import fastapi.applications
from fastapi import FastAPI
from config import settings

from fastapi.staticfiles import StaticFiles
from core import setup
from core.environment import ConfigProvider
import logging

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



@app.on_event("startup")
async def startup_event():
    # Define environment
    await init_options(environment)
    # Define View, Routers
    await setup.init(app)


if __name__ == "__main__":
    # the port is defined by command
    uvicorn.run("main:app", host="0.0.0.0", reload=True)

"""
# Ejemplo de uso
config_manager = ConfigProvider()
config_manager.set_config('database', 'host', 'localhost')
config_manager.set_config('database', 'port', 5432)
config_manager.set_config('general', 'debug_mode', True)

config_manager.show_configs()
# Obtiene un valor específico
print(config_manager.get_config('database', 'host'))

    TODO: Health
    TODO: API Product
    TODO: NOSQL
    TODO: API Category
"""
