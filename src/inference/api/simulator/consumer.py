import json
import logging
from typing import Any

from api.simulator.model import ResponsePrediction, PredictRequest
from core.eventbus import nats_provider
from core.eventbus import topic_predict_response
from core.model_ai_provider import model_provider
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
    logging.info(f"Predict: Starting process")
    data = json.loads(msg.data.decode())
    logging.info(f"Predict: Received subject request: {msg.subject} ")
    logging.info(f"Predict: Received predict request: {data}")

    categories = ["Category 1", "Category 2", "Category 3", "Category 4", "Category 5"]
    payload = {
        "prediction_id": data["id"],
        "categories": categories

    }

    model_1 = model_provider.get_model("model1")
    if model_1:
        logging.info("Model 1 loaded and ready for use.")
    else:
        logging.error("Model 1 could not be loaded.")

    # pred_request = init_prediction_request(data)
    # text_field_normalize(pred_request)

    logging.info(f"Predict: Ending process")

    resp_prediction = ResponsePrediction(id=data["id"], payload=json.dumps(payload))
    logging.info(f"Predict result: {resp_prediction}")
    try:

        subject = topic_predict_response
        message = resp_prediction.model_dump_json()
        await nats_provider.publish(subject, message)

        logging.info(f"Predict result: {resp_prediction} ")
    except Exception as e:
        logging.error(f"Predict request error: {e}")
