from pydantic import BaseModel, UUID4, Field
from typing import Dict, Any
from uuid import uuid4


class PredictRequest(BaseModel):
    id: str
    name: str
    description: str
    price: str
    type: str
    manufacturer: str


