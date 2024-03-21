import asyncio
import os
import pickle
from concurrent.futures import ThreadPoolExecutor
from typing import Dict

from core.logger_provider import logger

scaler_files_paths = {
    "scaler0": "/assets/model/scaler_0.pkl",
    "scaler1": "/assets/model/scaler_1.pkl",
    "scaler2": "/assets/model/scaler_2.pkl",
    "scaler3": "/assets/model/scaler_3.pkl",
    "scaler4": "/assets/model/scaler_4.pkl",
}


# noinspection DuplicatedCode
class ScalerManager:
    def __init__(self, base_path: str, scaler_dict: Dict[str, str]):
        self.base_path = base_path
        self.scaler_dict = scaler_dict
        self.scaler = {}
        self.load_success = True

    async def load_scaler_async(self) -> None:
        """
        Asynchronously loads scaler files defined in scaler_dict.
        """
        loop = asyncio.get_event_loop()

        with ThreadPoolExecutor() as pool:
            futures = []
            for key, path in self.scaler_dict.items():
                full_path = f"{self.base_path}{path}"
                future = loop.run_in_executor(pool, self.load_scaler_file, key, full_path)
                futures.append((key, future))

            all_loaded_successfully = True
            for key, future in futures:
                try:
                    await future
                except Exception as e:
                    logger.error(f"Failed to load scaler {key}. Exception: {e}")
                    all_loaded_successfully = False
                    break

            self.load_success = all_loaded_successfully

    def load_scaler_file(self, key: str, full_path: str):
        """
        Loads a single scaler file.
        """
        try:
            with open(full_path, 'rb') as file:
                self.scaler[key] = pickle.load(file)
                logger.info(f"Scaler file {key} loaded successfully.")
        except Exception as e:
            logger.error(f"Failed to load Scaler file {key}. Exception: {e}")
            self.load_success = False


scaler_provider = ScalerManager(os.getcwd(), scaler_files_paths)
