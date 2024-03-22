import os
from typing import Dict, Optional

from tensorflow.keras.models import load_model

from core.logger_provider import logger
from core.singleton import SingletonMeta

model_paths = {
    "model0": "/assets/models/model_1_preberttune.h5",
    "model1": "/assets/models/model_2_preberttune.h5",
    "model2": "/assets/models/model_3_preberttune.h5",
    "model3": "/assets/models/model_4_preberttune.h5",
    "model4": "/assets/models/model_5_preberttune.h5",
}


class ModelManager(metaclass=SingletonMeta):
    def __init__(self):
        self.is_loaded = None
        self.base_path = None
        if not hasattr(self, 'models'):
            self.models = {}
            self.base_path = os.getcwd()
            self.load_models(model_paths)

    def load_models(self, model_path: Dict[str, str]) -> None:
        all_loaded = True
        self.base_path = os.getcwd()
        for key, path in model_path.items():
            full_path = f"{self.base_path}{path}"
            logger.info(f"Loading model {key} from full path: {full_path}.")
            try:
                self.models[key] = load_model(full_path)
                logger.info(f"Model {key} loaded successfully from {full_path}.")
            except Exception as e:
                logger.error(f"Failed to load model {key} from full path: {full_path}. Error: {e}")
                all_loaded = False
                break

        self.is_loaded = all_loaded

    def get_model(self, key: str) -> Optional[Dict]:
        return self.models.get(key, None)


model_admin = ModelManager()
