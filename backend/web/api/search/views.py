from typing import List

from fastapi import APIRouter
from fastapi.param_functions import Depends

from backend.web.api.search.schema import Keywords, Query
from backend.web.api.search.rag import KeywordExtractor

router = APIRouter()
keyword_extractor = KeywordExtractor()

@router.post("/", response_model=Keywords)
def get_keywords(
    query: Query,
) -> str:
    """
    Return keywords from given query

    :param query: Query from user.
    :return: Keywords from query.
    """
    return keyword_extractor.extract_keywords(input=query.query)
