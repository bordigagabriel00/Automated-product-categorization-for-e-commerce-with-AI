import os
from typing import Dict, Optional

from tensorflow.keras.models import load_model

from core.logger_provider import logger

# Define the paths to your models here
model_paths = {
    "model1": "/assets/model/model_1_preberttune.h5",
    "model2": "/assets/model/model_2_preberttune.h5",
    "model3": "/assets/model/model_3_preberttune.h5",
    "model4": "/assets/model/model_4_preberttune.h5",
    "model5": "/assets/model/model_5_preberttune.h5",
}


class SingletonMeta(type):
    """
    A metaclass that creates a Singleton instance.
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class ModelManager(metaclass=SingletonMeta):
    def __init__(self, model_path: Dict[str, str], base_path: str = ""):
        """
        Initializes the ModelManager with a dictionary of model keys and their file paths,
        and optionally a base path that is prepended to each model path.

        Args:
            model_path (Dict[str, str]): A dictionary where keys are model identifiers and values are file paths to the models.
            base_path (str, optional): Base path to prepend to each model path.
        """
        if not hasattr(self, 'models'):
            self.models = {}
            self.base_path = base_path
            self.load_models(model_path)

    def load_models(self, model_path: Dict[str, str]) -> None:
        """
        Synchronously loads models based on the provided dictionary of model paths.

        Args:
            model_path (Dict[str, str]): A dictionary where keys are model identifiers and values are file paths to the models.
        """
        for key, path in model_path.items():
            full_path = f"{self.base_path}{path}"
            logger.info(f"Loading model {key} from full path: {full_path}.")
            try:
                self.models[key] = load_model(full_path)
                logger.info(f"Model {key} loaded successfully from {path}.")
            except Exception as e:
                logger.error(f"Failed to load model {key} from Full path: {full_path}")

    def get_model(self, key: str) -> Optional[Dict]:
        """
        Retrieves a model based on its key.

        Args:
            key (str): The key identifier for the model.

        Returns:
            The model associated with the provided key or None if the key is not found.
        """
        return self.models.get(key, None)


file_path = os.getcwd()

model_provider = ModelManager(model_paths, file_path)
