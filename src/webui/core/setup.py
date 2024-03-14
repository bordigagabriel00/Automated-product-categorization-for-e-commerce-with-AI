from fastapi import FastAPI

from api.category.router import category_router
from api.health.router import health_router
from api.monitor.consumer import topic_health, monitor_message_handler
from api.product.router import product_router
from api.simulator.router import predict_router
from core.eventbus import nats_provider
from core.views_router import main_router


def config_router(app: FastAPI) -> None:
    # Health definitions
    app.include_router(health_router)
    # Router Simulator
    app.include_router(predict_router)
    # Router definitions
    app.include_router(product_router)
    #  Category definitions
    app.include_router(category_router)

    return


def config_views(app: FastAPI) -> None:
    # Views
    app.include_router(main_router)


async def init(app: FastAPI) -> None:
    # Define Routers
    config_router(app)


    # Define View
    config_views(app)
