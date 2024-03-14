from fastapi import FastAPI

from api.health.router import health_router
from api.monitor.consumer import  monitor_message_handler
from api.simulator.consumer import predict_request_handler
from core.eventbus import nats_provider, topic_predict_request, topic_health


def config_router(app: FastAPI) -> None:
    # Health definitions
    app.include_router(health_router)

    return


async def config_event_bus() -> None:
    # Health Subscriber
    await nats_provider.subscribe(topic_health, monitor_message_handler)

    # Predict Request Subscriber
    await nats_provider.subscribe(topic_predict_request, predict_request_handler)

    return


async def init(app: FastAPI) -> None:
    # Define Routers
    config_router(app)

    # Define Event Bus
    await config_event_bus()
