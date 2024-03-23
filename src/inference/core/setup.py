from fastapi import FastAPI

from api.health.router import health_router
from api.monitor.consumer import monitor_message_handler
from api.simulator.consumer import bert_base_prediction_request_handler, bert_ft_prediction_request_handler
from core.eventbus import (nats_provider,
                           bert_base_prediction_request_topic,
                           topic_health,
                           bert_ft_prediction_request_topic)


def config_router(app: FastAPI) -> None:
    # Health definitions
    app.include_router(health_router)

    return


async def config_event_bus() -> None:
    # Health Subscriber
    await nats_provider.subscribe(topic_health, monitor_message_handler)

    # Bert Base Prediction  Request Subscriber
    await nats_provider.subscribe(bert_base_prediction_request_topic, bert_base_prediction_request_handler)

    # Bert ft Prediction  Request Subscriber
    await nats_provider.subscribe(bert_ft_prediction_request_topic, bert_ft_prediction_request_handler)

    return


async def init(app: FastAPI) -> None:
    # Define Routers
    config_router(app)

    # Define Event Bus
    await config_event_bus()
