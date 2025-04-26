from pydantic import BaseModel, ConfigDict, Field
from typing import Optional


class Keywords(BaseModel):
    """
    Model which response keywords.

    """

    response: list[str] = Field(description="List of the most relevant keywords extracted from the query.")

    # model_config = ConfigDict(from_attributes=True)

class Query(BaseModel):
    """User query."""

    query: str

class QueryExpension(BaseModel):
    """E-commerce query expansion and product information generation"""
    
    expended_query: str = Field(description="The enriched query including synonyms and attributes.")
    product_title: str = Field(description="A concise, SEO-friendly title for the top maching product")
    product_detail: str = Field(description="A detailed description including key feature, specification and user case")

    def to_string(self) -> str:
        """Generates a formatted string representation of the object."""
        # You can format the string however you like
        return f"Expanded Query:{self.expended_query}\nProduct Title:{self.product_title}->Product Detail : {self.product_detail}"

class Vectors(BaseModel):
    """User query."""

    id: int

    title: Optional[str] = None
    category: Optional[str] = None
    brand: Optional[str] = None
    description: Optional[str] = None

class Historys(BaseModel):
    """User query."""

    id: int
    query: str
