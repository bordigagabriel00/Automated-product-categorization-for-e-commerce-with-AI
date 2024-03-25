from pydantic import BaseModel


class Product(BaseModel):
    id: str
    name: str
    type: str
    sku: str
    upc: str
