from typing import List

from fastapi import APIRouter
from fastapi.param_functions import Depends

from backend.web.api.search.schema import Keywords, Query, QueryExpension
from backend.web.api.search.rag import SearchPipeline
from backend.settings import settings

router = APIRouter()
search_pipeline = SearchPipeline()

@router.post("/", response_model=Keywords)
def get_keywords(
    query: Query,
) -> str:
    """
    Return keywords from given query

    :param query: Query from user.
    :return: Keywords from query.
    """
    return search_pipeline.extract_keywords(input=query.query)


@router.post("/expend", response_model= QueryExpension)
def get_query_expension(
    query: Query,
) -> str:
    """
    Return Reformulated query from given query and the product description

    :param query: Query from user.
    :return: Reformulated query and product description.
    """
    return search_pipeline.query_expension(input=query.query)

@router.post("/emb", response_model= QueryExpension)
def get_query_expension(
    query: Query,
) -> str:
    """
    Return Reformulated query from given query and the product description

    :param query: Query from user.
    :return: Reformulated query and product description.
    """
    return search_pipeline.generate_embedding(input=query.query)


