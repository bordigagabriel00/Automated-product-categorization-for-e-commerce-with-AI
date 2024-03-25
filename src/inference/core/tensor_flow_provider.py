from typing import Dict

from tensorflow.keras.models import load_model as load_model_tf

from core.logger_provider import logger


def load_tensorflow_model(full_path: str) -> Dict:
    logger.info(f"Loading model from {full_path}")

    return load_model_tf(full_path)
