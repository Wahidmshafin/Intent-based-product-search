from pydantic import BaseModel, ConfigDict


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

