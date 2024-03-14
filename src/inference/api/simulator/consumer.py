import json
import logging

from api.simulator.model import ResponsePrediction
from core.eventbus import nats_provider
from core.eventbus import topic_predict_response


async def predict_request_handler(msg):
    data = json.loads(msg.data.decode())
    logging.info(f"Received subject request: {msg.subject} ")
    logging.info(f"Received predict request: {data}")

    data_dummy = [
        {
            "category": "Electronics",
            "subcategories": [
                {
                    "category": "Computers",
                    "subcategories": [
                        {
                            "category": "Laptops",
                            "subcategories": [
                                {
                                    "category": "Gaming",
                                    "subcategories": [
                                        {"category": "High-End", "level": "5"}
                                    ]
                                }]
                        }, ]
                }]
        }
    ]
    logging.info(f"Predict process")

    resp_prediction = ResponsePrediction(id=data["id"], payload=json.dumps(data_dummy))
    logging.info(f"Predict result: {resp_prediction}")
    try:

        subject = topic_predict_response
        message = resp_prediction.model_dump_json()
        await nats_provider.publish(subject, message)

        logging.info(f"Predict result: {resp_prediction} ")
    except Exception as e:
        logging.error(f"Predict request error: {e}")
