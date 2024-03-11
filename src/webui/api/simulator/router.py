import json
import logging
import uuid

from fastapi import APIRouter, HTTPException

import config
from api.simulator.model import PredictRequest
from core.eventbus import nats_provider as nats, topic_predict_request

predict_router = APIRouter()


@predict_router.post(f"{config.settings.base_url}/predict", tags=['api'])
async def send_predict(predict: PredictRequest):
    predict_response = {"id": ""}
    logging.info(f"Predict request: '{str(predict.json())}'")
    try:
        # Publish topic

        await nats.nc.publish(topic_predict_request, json.dumps(predict.dict()).encode())


        predict_response["id"] = str(uuid.uuid4())



    except Exception as e:
        logging.error(f"Predict request error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

    return json.dumps(predict_response)

"""
@predict_router.post(f"{config.settings.base_url}/predict/retrieve/" + "{predict_id}", tags=['api'])
async def retrieve_predict(predict: PredictRequest):
    predict_response = {"id": ""}
    logging.info(f"Predict request: '{str(predict.json())}'")
    try:
        # Publish topic
        await nats.nc.publish(topic_predict_request, json.dumps(predict.dict()).encode())
        await nats.nc.drain()

        predict_response["id"] = str(uuid.uuid4())

        await nats.nc.drain()

    except Exception as e:
        logging.error(f"Predict request error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

    return json.dumps(predict_response)

"""
