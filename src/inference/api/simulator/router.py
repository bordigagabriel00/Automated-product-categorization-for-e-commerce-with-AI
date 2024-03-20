import logging

from fastapi import APIRouter

import config
from api.simulator.model import PredictRequest
from core.eventbus import nats_provider as nats, topic_predict_request

predict_router = APIRouter()


@predict_router.post(f"{config.settings.base_url}predict", tags=['api'])
async def send_predict(predict: PredictRequest):
    logger.info(f"Predict request: '{predict}'")
    await nats.publish(topic_predict_request, " Send Message from api predict")
    return {"message": "UP"}
