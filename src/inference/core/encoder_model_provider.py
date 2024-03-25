import os
import pickle
from typing import Dict, Optional

from core.logger_provider import logger
from core.singleton import SingletonMeta

# File paths for different models:
encoder_files_paths = {
    "model0": "/assets/encoder/encoder.pkl",
    "model1": "/assets/encoder/encoder_1.pkl",
    "model2": "/assets/encoder/encoder_2.pkl",
    "model3": "/assets/encoder/encoder_3.pkl",
    "model4": "/assets/encoder/encoder_4.pkl",
}

# Class to handle encoders, implementing the Singleton pattern:
# During execution shows: "noinspection DuplicatedCode" (Due to time issues, a multiclass was not performed, so we iterated over the same function)
class EncoderManager(metaclass=SingletonMeta):
    def __init__(self):
        self.is_loaded = None
        self.base_path = None
        if not hasattr(self, 'encoder'):
            self.encoder = {}
            self.load_encoders(encoder_files_paths)

    # Encoders loading and execution log:
    def load_encoders(self, model_path: Dict[str, str]) -> None:
        all_loaded = True  
        self.base_path = os.getcwd()   
        for key, path in model_path.items():
            full_path = f"{self.base_path}{path}"
            logger.info(f"Loading model {key} from full path: {full_path}.")
            try:
                with open(full_path, 'rb') as file:
                    self.encoder[key] = pickle.load(file)
                    logger.info(f"Encoder file {key} loaded successfully.")
            except Exception as e:
                logger.error(f"Failed to load model {key} from full path: {full_path}. Error: {e}")
                all_loaded = False
                break   
                
        self.is_loaded = all_loaded  

    # 'get_encoder' function: returns the requested encoder or None if not found
    def get_encoder(self, key: str) -> Optional[Dict]:
        return self.encoder.get(key, None)


encoder_provider = EncoderManager()


