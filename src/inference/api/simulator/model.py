from pydantic import BaseModel, UUID4


class PredictRequest(BaseModel):
    id: str
    name: str
    description: str
    price: str
    type: str
    manufacturer: str


class ResponsePrediction(BaseModel):
    id: UUID4
    payload: str
