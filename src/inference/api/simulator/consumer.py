import json
from typing import Any

from api.simulator.model import PredictRequest
from core.eventbus import nats_provider
from core.eventbus import topic_predict_response
from core.inference_service import predict_with_models
from core.logger_provider import logger
from core.normalization_provider import normalize_text


def text_field_normalize(request: PredictRequest):
    request.normalized_name = normalize_text(request.name)
    request.normalized_description = normalize_text(request.description)


def init_prediction_request(data: Any) -> PredictRequest:
    pred_request = PredictRequest(id="")
    pred_request.id = data['id']
    pred_request.name = data['name']
    pred_request.description = data['description']
    pred_request.price = data['price']
    pred_request.product_type = data['product_type']
    pred_request.manufacturer = data['manufacturer']

    return pred_request


async def predict_request_handler(msg):
    logger.info(f"Predict Handler: Starting process")
    data = json.loads(msg.data.decode())
    logger.info(f"Predict Handler: Received subject request: {msg.subject} ")
    logger.info(f"Predict Handler: Received predict request: {data}")

    categories = ["Category 1", "Category 2", "Category 3", "Category 4", "Category 5"]
    predict_request = {
        "prediction_id": data["id"],
        "payload":  data["payload"]

    }

    resp_prediction = predict_with_models(predict_request)

    logger.info(f"Predict: Ending process")

    logger.info(f"Predict result: {resp_prediction}")
    try:

        subject = topic_predict_response
        message = resp_prediction.model_dump_json()
        await nats_provider.publish(subject, message)

        logger.info(f"Predict result: {resp_prediction} ")
    except Exception as e:
        logger.error(f"Predict request error: {e}")
