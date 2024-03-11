from pydantic import BaseModel


class PredictRequest(BaseModel):
    id:str
    name: str
    description: str
    price: str
    type: str
    manufacturer: str
