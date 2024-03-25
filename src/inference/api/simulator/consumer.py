import json
from typing import Any

from api.simulator.model import PredictRequest
from core.eventbus import bert_base_prediction_response_topic, bert_ft_prediction_response_topic
from core.eventbus import nats_provider
from core.inference_service import predict_with_models
from core.inference_service_tunning import predict_ft_with_models
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


async def bert_base_prediction_request_handler(msg):
    section = "BERT-BASE"
    data = msg_init(f"{section}", msg)

    predict_request = {
        "prediction_id": data["id"],
        "payload": data["payload"]

    }

    resp_prediction = predict_with_models(predict_request)

    logger.info(f"{section} Predict result: {resp_prediction}")
    try:
        subject = bert_base_prediction_response_topic
        message = resp_prediction.model_dump_json()
        await nats_provider.publish(subject, message)

        logger.info(f"{section} Predict result: {resp_prediction} ")
    except Exception as e:
        logger.error(f"{section} Predict request error: {e}")
    logger.info(f"{section} Predict: Ending process")


async def bert_ft_prediction_request_handler(msg):
    section = "BERT_FT"
    data = msg_init(f"{section}", msg)

    predict_request = {
        "prediction_id": data["id"],
        "payload": data["payload"]

    }

    resp_prediction = predict_ft_with_models(predict_request)

    logger.info(f"[{section}] Predict result: {resp_prediction}")
    try:
        subject = bert_ft_prediction_response_topic
        message = resp_prediction.model_dump_json()
        await nats_provider.publish(subject, message)

        logger.info(f"[{section}] Predict result: {resp_prediction} ")
    except Exception as e:
        logger.error(f"[{section}] Predict request error: {e}")
    logger.info(f"[{section}] Predict: Ending process")


def msg_init(section, msg):
    logger.info(f"[{section}] Predict Handler: Starting process")
    data = json.loads(msg.data.decode())
    logger.info(f"[{section}] Predict Handler: Received subject request: {msg.subject} ")
    logger.info(f"[{section}] Predict Handler: Received predict request: {data}")

    return data
