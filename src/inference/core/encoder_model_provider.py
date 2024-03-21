import asyncio
import os
import pickle
from concurrent.futures import ThreadPoolExecutor
from typing import Dict

from core.logger_provider import logger

encoder_files_paths = {
    "encoder0": "/assets/model/encoder_0.pkl",
    "encoder1": "/assets/model/encoder_1.pkl",
    "encoder2": "/assets/model/encoder_2.pkl",
    "encoder3": "/assets/model/encoder_3.pkl",
    "encoder4": "/assets/model/encoder_4.pkl",
}


# noinspection DuplicatedCode
class EncoderManager:
    def __init__(self, base_path: str, encoder_dict: Dict[str, str]):
        self.base_path = base_path
        self.encoder_dict = encoder_dict
        self.encoder = {}
        self.load_success = True

    async def load_encoder_async(self) -> None:
        """
        Asynchronously loads encoder files defined in encoder_dict.
        """
        loop = asyncio.get_event_loop()

        with ThreadPoolExecutor() as pool:
            futures = []
            for key, path in self.encoder_dict.items():
                full_path = f"{self.base_path}{path}"
                future = loop.run_in_executor(pool, self.load_encoder_file, key, full_path)
                futures.append((key, future))

            all_loaded_successfully = True
            for key, future in futures:
                try:
                    await future
                except Exception as e:
                    logger.error(f"Failed to load encoder {key}. Exception: {e}")
                    all_loaded_successfully = False
                    break

            self.load_success = all_loaded_successfully

    def load_encoder_file(self, key: str, full_path: str):
        """
        Loads a single encoder file.
        """
        try:
            with open(full_path, 'rb') as file:
                self.encoder[key] = pickle.load(file)
                logger.info(f"encoder file {key} loaded successfully.")
        except Exception as e:
            logger.error(f"Failed to load encoder file {key}. Exception: {e}")
            self.load_success = False


encoder_provider = EncoderManager(os.getcwd(), encoder_files_paths)
