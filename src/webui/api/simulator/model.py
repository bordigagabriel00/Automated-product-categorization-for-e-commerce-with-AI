from typing import Dict, Any
from uuid import uuid4

from pydantic import BaseModel, UUID4, Field


class PredictionRequest(BaseModel):
    name: str
    description: str
    price: str
    product_type: str
    manufacturer: str


class RequestModel(BaseModel):
    id: UUID4 = Field(default_factory=uuid4)
    payload: Dict[str, Any]
