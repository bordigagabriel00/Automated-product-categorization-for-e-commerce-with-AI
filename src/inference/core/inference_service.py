import json

from api.simulator.model import ResponsePrediction
from core.logger_provider import logger
from core.model_ai_provider import model_provider


def predict_with_models(payload):
    models = ["model1", "model2", "model3", "model4", "model5"]
    for _, code in enumerate(models):
        model = model_provider.get_model(code)
        if model:
            logger.info(F"{code} loaded and ready for use.")
            predict_categories(model, payload, code)
        else:
            logger.error(f"{code} could not be loaded.")

    return ResponsePrediction(id=payload["prediction_id"], payload=json.dumps(payload))


def predict_categories(model, payload, code):
    logger.info(f"Predicting model: {code}")
    logger.info(model)
    logger.info(payload)
    return
