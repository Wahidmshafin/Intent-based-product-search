from pydantic import BaseModel, ConfigDict
from backend.db.models.dummy_model import ProductTable
from typing import Optional
class ProductUpload(BaseModel):
    """
    DTO for dummy models.

    It returned when accessing dummy models from the API.
    """

    response: str

class Products(BaseModel):
    """Products"""
    id: int
    new_id: int
    category: str
    brand: str
    description: str
    title: str
    price: str
    spec: str
    embedding: list[float]
    

# class ProductItem(BaseModel):
#     """Products (Pydantic Schema)"""
#     id: int
#     title: str 
#     category:str
#     brand:str
#     description: str

#     class Config:
#         orm_mode = True

class ProductItem(BaseModel):
    """Products (Pydantic Schema)"""
    id: int

    title: Optional[str] = None
    category: Optional[str] = None
    brand: Optional[str] = None
    description: Optional[str] = None

