import json
import logging

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

    predict_response = dict()
    predict_response["prediction_id"] = data["id"]
    predict_response["data"] = data_dummy
    logging.info(f"Predict result: {predict_response}")
    try:

        subject = topic_predict_response
        message = json.dumps(predict_response)
        await nats_provider.publish(subject, message)

        logging.info(f"Predict result: {predict_response} ")
    except Exception as e:
        logging.error(f"Predict request error: {e}")
