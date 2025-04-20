from pydantic import BaseModel, ConfigDict


class Keywords(BaseModel):
    """
    Model which response keywords.

    """

    response: str

    model_config = ConfigDict(from_attributes=True)


class Query(BaseModel):
    """User query."""

    query: str
