import uvicorn
import pathlib
import fastapi.applications
from fastapi import FastAPI
from config import settings


from fastapi.staticfiles import StaticFiles
from core import setup


# Define the app at the module level
app: fastapi.applications.FastAPI = FastAPI(title=settings.app_name,
                                            description=settings.description,
                                            version=settings.app_version)

BASE_DIR = pathlib.Path(__file__).parent
BASE_STATIC_DIR = BASE_DIR / 'ui' / 'static'


app.mount("/static", StaticFiles(directory=BASE_STATIC_DIR), name="static")



@app.on_event("startup")
def startup_event():
    # Setup routers
    setup.config_router(app)

    # Setup event bus
    setup.config_event_bus(app)

    # Config views
    setup.config_views(app)




if __name__ == "__main__":
    # the port is defined by command
    uvicorn.run("main:app", host="0.0.0.0", reload=True)

"""
    TODO: Health
    TODO: API Product
    TODO: NOSQL
    TODO: API Category
"""
