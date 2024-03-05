from fastapi import FastAPI
from api.product.router import product_router
from api.health.router import health_router
from api.category.router import category_router
from views_router import main_router


def config_router(app: FastAPI) -> None:
    # Health definitions
    app.include_router(health_router)
    # Router definitions
    app.include_router(product_router)
    #  Category definitions
    app.include_router(category_router)

    return


def config_event_bus(app: FastAPI) -> None:
    return


def config_views(app: FastAPI) -> None:
    # Views
    app.include_router(main_router)
