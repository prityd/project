from pydantic import BaseModel
from typing import List

class Size(BaseModel):
    size: str
    quantity: int

class Product(BaseModel):
    name: str
    price: float
    sizes: List[Size]

class OrderItem(BaseModel):
    productId: str
    qty: int

class Order(BaseModel):
    userId: str
    items: List[OrderItem]