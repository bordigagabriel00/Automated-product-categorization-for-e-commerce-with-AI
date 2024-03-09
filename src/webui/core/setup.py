from fastapi import FastAPI

from api.category.router import category_router
from api.health.router import health_router
from api.monitor.consumer import topic_health, monitor_message_handler
from api.product.router import product_router
from core.eventbus import nats_provider
from views_router import main_router


def config_router(app: FastAPI) -> None:
    # Health definitions
    app.include_router(health_router)
    # Router definitions
    app.include_router(product_router)
    #  Category definitions
    app.include_router(category_router)

    return


async def config_event_bus() -> None:
    # Health Subscriber
    await nats_provider.subscribe(topic_health, monitor_message_handler)

    return


def config_views(app: FastAPI) -> None:
    # Views
    app.include_router(main_router)


async def init(app: FastAPI) -> None:
    # Define Routers
    config_router(app)

    # Define Event Bus
    await config_event_bus()

    # Define View
    config_views(app)
