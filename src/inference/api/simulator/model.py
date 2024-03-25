from typing import Optional

from pydantic import BaseModel
from pydantic import UUID4


class PredictRequest(BaseModel):
    """
    A request model for making predictions. This model validates the input data for a prediction request.

    Attributes:
        id (str): A unique identifier for the prediction request.
        name (str, optional): The name of the product.
        description (str, optional): The description of the product.
        price (str, optional): The price of the product as a string. It should represent a decimal or integer value.
        manufacturer (str, optional): The name of the product manufacturer.
        product_type (str, optional): The type/category of the product.
        normalized_name (str, optional): A normalized version of the product name for consistency in predictions.
        normalized_description (str, optional): A normalized version of the product description.
        normalized_price (float, optional): A normalized and validated numerical representation of the product's price.
        normalized_product_type (str, optional): A normalized version of the product type.
        normalized_manufacturer (str, optional): A normalized version of the manufacturer's name.
    """
    id: str
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[str] = None
    manufacturer: Optional[str] = None
    product_type: Optional[str] = None
    normalized_name: Optional[str] = None
    normalized_description: Optional[str] = None
    normalized_price: Optional[float] = None
    normalized_product_type: Optional[str] = None
    normalized_manufacturer: Optional[str] = None


class ResponsePrediction(BaseModel):
    """
    A response model for predictions. This model formats the prediction response.

    Attributes:
        id (UUID4): A unique identifier for the prediction response, using UUID4 format.
        categories (str): The payload of the prediction response, typically the predicted value or outcome.
    """
    id: UUID4
    categories: list[str]
