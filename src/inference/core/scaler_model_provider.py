import asyncio
import os
import pickle
from concurrent.futures import ThreadPoolExecutor
from typing import Dict, Any, Optional

from core.logger_provider import logger
from core.singleton import SingletonMeta

scaler_files_paths = {
    "model0": "/assets/scaler/scaler.pkl",
    "model1": "/assets/scaler/scaler_1.pkl",
    "model2": "/assets/scaler/scaler_2.pkl",
    "model3": "/assets/scaler/scaler_3.pkl",
    "model4": "/assets/scaler/scaler_4.pkl",
}


# noinspection DuplicatedCode
class ScalerManager(metaclass=SingletonMeta):
    def __init__(self, ):
        self.is_loaded = None
        self.base_path = None
        if not hasattr(self, 'scalers'):
            self.scalers = {}
            self.load_scaler(scaler_files_paths)

    def load_scaler(self, model_path: Dict[str, str]) -> None:
        all_loaded = True
        self.base_path = os.getcwd()
        for key, path in model_path.items():
            full_path = f"{self.base_path}{path}"
            logger.info(f"Loading model {key} from full path: {full_path}.")
            try:
                with open(full_path, 'rb') as file:
                    self.scalers[key] = pickle.load(file)
                    logger.info(f"Encoder file {key} loaded successfully.")
            except Exception as e:
                logger.error(f"Failed to load model {key} from full path: {full_path}. Error: {e}")
                all_loaded = False
                break

        self.is_loaded = all_loaded

    def get_scaler(self, key: str) -> Optional[Dict]:
        return self.scalers.get(key, None)


scaler_provider = ScalerManager()
