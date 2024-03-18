from typing import Dict

from tensorflow.keras.models import load_model

# Define the paths to your models here
model_paths = {
    "model1": "assets/models/model_1_preberttune.h5",
    "model2": "assets/models/model_2_preberttune.h5",
    "model3": "assets/models/model_3_preberttune.h5",
    "model4": "assets/models/model_4_preberttune.h5",
    "model5": "assets/models/model_5_preberttune.h5",
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
    def __init__(self, model_path: Dict[str, str] = None):
        """
        Initializes the ModelManager with a dictionary of model keys and their file paths.
        If the ModelManager has already been instantiated, it skips re-initialization.

        Args:
            model_path (Dict[str, str], optional): A dictionary where keys are model identifiers and values are file paths to the models.
        """
        if not hasattr(self, 'models'):  # Check if the instance is already initialized
            self.models = {}
            if model_path:
                self.load_models(model_path)

    def load_models(self, model_path: Dict[str, str]) -> None:
        """
        Loads models based on the provided dictionary of model paths.

        Args:
            model_path (Dict[str, str]): A dictionary where keys are model identifiers and values are file paths to the models.
        """
        for key, path in model_path.items():
            try:
                self.models[key] = load_model(path)
                print(f"Model {key} loaded successfully.")
            except Exception as e:
                print(f"Failed to load model {key}: {e}")

    def get_model(self, key: str):
        """
        Retrieves a model based on its key.

        Args:
            key (str): The key identifier for the model.

        Returns:
            The model associated with the provided key or None if the key is not found.
        """
        return self.models.get(key, None)


# Initialize the ModelManager with the model paths
model_provider = ModelManager(model_paths)
