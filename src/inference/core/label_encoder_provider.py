import asyncio
import os
from concurrent.futures import ThreadPoolExecutor
from typing import Dict, Any

import h5py

from core.logger_provider import logger

label_encoder_files_paths = {
    "model0": "/assets/model/label_encoder_0.h5",
    "model1": "/assets/model/label_encoder_1.h5",
    "model2": "/assets/model/label_encoder_2.h5",
    "model3": "/assets/model/label_encoder_3.h5",
    "model4": "/assets/model/label_encoder_4.h5",
}


class LabelEncoderManager:
    """
    Manages the loading and retrieval of label encoder files.

    Attributes:
        base_path (str): Base directory path to prefix to each label encoder's file path.
        label_encoder_dict (Dict[str, str]): Dictionary of label encoder identifiers and their file paths.
        label_encoders (Dict[str, np.ndarray]): Dictionary of loaded label encoder numpy arrays.
        load_success (bool): Flag indicating if all label encoders were loaded successfully.
    """

    def __init__(self, base_path: str, label_encoder_dict: Dict[str, Any]):
        self.base_path = base_path
        self.label_encoder_dict = label_encoder_dict
        self.label_encoders = {}
        self.load_success = True

    async def load_label_encoders_async(self) -> None:
        """
        Asynchronously loads label encoder files defined in label_encoder_dict.
        """
        loop = asyncio.get_event_loop()

        with ThreadPoolExecutor() as pool:
            futures = []
            for key, path in self.label_encoder_dict.items():
                full_path = f"{self.base_path}{path}"
                future = loop.run_in_executor(pool, self.load_label_encoder_file, key, full_path)
                futures.append((key, future))

            all_loaded_successfully = True
            for key, future in futures:
                try:
                    await future
                except Exception as e:
                    logger.error(f"Failed to load label encoder for model  {key}. Exception: {e}")
                    all_loaded_successfully = False
                    break

            self.load_success = all_loaded_successfully

    def load_label_encoder_file(self, key: str, full_path: str):
        """
        Loads a single label encoder file.
        """
        try:
            with h5py.File(full_path, 'r') as hf:
                self.label_encoders[key] = hf['label_encoder'][:]
                logger.info(f"Label encoder file for model  {key} loaded successfully.")
        except Exception as e:
            logger.error(f"Failed to load label encoder file for model {key}. Exception: {e}. path: {full_path}")
            self.load_success = False

    def get_label_encoder(self, key: str) -> Any:
        """
        Retrieves a loaded label encoder by its key.

        Args:
            key (str): The unique identifier for the label encoder.

        Returns:
            np.ndarray: The loaded label encoder numpy array or raises an HTTPException if not found.
        """
        if key in self.label_encoders:
            return self.label_encoders[key]
        else:
            return None


label_encoder_provider = LabelEncoderManager(os.getcwd(), label_encoder_files_paths)
