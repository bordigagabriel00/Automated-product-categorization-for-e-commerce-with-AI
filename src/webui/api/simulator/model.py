from pydantic import BaseModel


class PredictRequest(BaseModel):
    name: str
    description: str
    price: str
    type: str
    manufacturer: str
