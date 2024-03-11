import logging

from fastapi import APIRouter

import config
from core.eventbus import nats_provider as nats, topic_predict_request
from api.simulator.model import PredictRequest

predict_router = APIRouter()


@predict_router.post(f"{config.settings.base_url}/predict", tags=['api'])
async def send_predict(predict: PredictRequest):
    logging.info(f"Predict request: '{str(predict.json())}'")
    await nats.publish(topic_predict_request, str(predict.json().encode()))
    return {"message": "UP"}
