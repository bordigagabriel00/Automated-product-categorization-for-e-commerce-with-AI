import logging
from api.simulator.model import PredictRequest


async def predict_request_handler(predict: PredictRequest):
    data = predict.data.decode()
    logging.info(f"Received message: {data}")

    logging.info(f"Predict process")

    logging.info(f"Predict result: ")
