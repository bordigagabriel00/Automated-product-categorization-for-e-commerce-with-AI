from fastapi import FastAPI

from api.health.router import health_router
from api.manufacturer.router import manufacturer_router
from api.product.router import product_router
from api.product_type.router import product_type_router
from core.views_router import main_router


def config_router(app: FastAPI) -> None:
    # Health definitions
    app.include_router(health_router)
    # Router definitions
    app.include_router(product_router)
    #  Type definitions
    app.include_router(product_type_router)
    #  Manufacturer definitions
    app.include_router(manufacturer_router)

    return


def config_views(app: FastAPI) -> None:
    # Views
    app.include_router(main_router)


async def init(app: FastAPI) -> None:
    # Define Routers
    config_router(app)

    # Define View
    config_views(app)
