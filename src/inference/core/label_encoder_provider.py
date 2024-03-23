import os
from typing import Dict, Optional, Any

import h5py

from core.logger_provider import logger
from core.singleton import SingletonMeta

label_encoder_files_paths = {
    "model0": "/assets/label_encoder/label_encoder.h5",
    "model1": "/assets/label_encoder/label_encoder_1.h5",
    "model2": "/assets/label_encoder/label_encoder_2.h5",
    "model3": "/assets/label_encoder/label_encoder_3.h5",
    "model4": "/assets/label_encoder/label_encoder_4.h5",
}


class LabelEncoderManager(metaclass=SingletonMeta):
    def __init__(self):
        self.is_loaded = False
        self.base_path = None
        if not hasattr(self, 'label_encoders'):
            self.label_encoders = {}
            self.load_label_encoders(label_encoder_files_paths)

    def load_label_encoder(self, full_path: str) -> Optional[Dict[str, Any]]:
        try:
            with h5py.File(full_path, 'r') as hf:
                return hf['label_encoder'][:]
        except Exception as e:
            logger.error(f"Failed to load label encoder from path: {full_path}. Error: {e}")
            return None

    def load_label_encoders(self, model_path: Dict[str, str]) -> None:
        all_loaded = True
        self.base_path = os.getcwd()
        for key, path in model_path.items():
            full_path = f"{self.base_path}{path}"
            logger.info(f"Loading model {key} from full path: {full_path}.")
            label_encoder = self.load_label_encoder(full_path)
            if label_encoder is not None:
                self.label_encoders[key] = label_encoder
                logger.info(f"Label encoder {key} loaded successfully.")
            else:
                all_loaded = False

        self.is_loaded = all_loaded

    def get_label_encoder(self, key: str) -> Optional[Dict]:
        return self.label_encoders.get(key, None)


label_encoder_provider = LabelEncoderManager()
