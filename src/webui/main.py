import uvicorn
import pathlib
import fastapi.applications
from fastapi import FastAPI
from config import settings
from api.product.router import product_router
from api.health.router import health_router
from api.category.router import category_router
from ui.view.home.router import home_router
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# Define the app at the module level
app: fastapi.applications.FastAPI = FastAPI(title=settings.app_name,
                                            description=settings.description,
                                            version=settings.app_version)

BASE_DIR = pathlib.Path(__file__).parent
BASE_STATIC_DIR = BASE_DIR / 'ui' / 'static'
BASE_TEMPLATE_DIR = BASE_DIR / 'ui' / 'templates'
print(BASE_DIR)
print(BASE_STATIC_DIR)
app.mount("/static", StaticFiles(directory=BASE_STATIC_DIR), name="static")
print(BASE_TEMPLATE_DIR)
templates = Jinja2Templates(directory=BASE_TEMPLATE_DIR )




@app.on_event("startup")
def startup_event():
    # Health definitions
    app.include_router(health_router)
    # Router definitions
    app.include_router(product_router)
    #  Category definitions
    app.include_router(category_router)

    # Views
    app.include_router(home_router)


if __name__ == "__main__":
    # the port is defined by command
    uvicorn.run("main:app", host="0.0.0.0", reload=True)

"""
    TODO: Health
    TODO: API Product
    TODO: NOSQL
    TODO: API Category
"""
