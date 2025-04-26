from pydantic import BaseModel, ConfigDict
from backend.db.models.dummy_model import ProductTable

class ProductUpload(BaseModel):
    """
    DTO for dummy models.

    It returned when accessing dummy models from the API.
    """

    response: str

class Products(BaseModel):
    """Products"""
    id: int
    colorname: str
    description: str
    name: str 
    fulldescription: str
    embedding: list[float]

class ProductItem(BaseModel):
    """Products (Pydantic Schema)"""
    id: int
    name: str 
    fulldescription: str

    class Config:
        orm_mode = True
