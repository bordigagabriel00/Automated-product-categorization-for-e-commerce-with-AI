from pydantic import BaseModel, UUID4, Field
from typing import Dict, Any
from uuid import uuid4

class PredictRequest(BaseModel):
    name: str
    description: str
    price: str
    type: str
    manufacturer: str



class RequestModel(BaseModel):
    id: UUID4 = Field(default_factory=uuid4)
    payload: Dict[str, Any]


