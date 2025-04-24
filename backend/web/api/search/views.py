from typing import List

from fastapi import APIRouter
from fastapi.param_functions import Depends

from backend.db.dao.product_dao import ProductDAO
from backend.web.api.search.schema import Keywords, Query, QueryExpension, Vectors
from backend.web.api.search.rag import SearchPipeline
from backend.settings import settings

router = APIRouter()
search_pipeline = SearchPipeline()


@router.post("/", response_model=List[Vectors])
async def hybrid_search(
    query: Query,
    product_dao: ProductDAO = Depends(),
) -> List[Vectors]:
    """
    Return keywords from given query

    :param query: Query from user.
    :return: Keywords from query.
    """
    keywords = search_pipeline.extract_keywords(query)

    better_query = search_pipeline.query_expension(query)
    
    embedding = search_pipeline.generate_embedding(better_query)
    # print(embedding)
    return await product_dao.hybrid_search(
        embedding=embedding,
        keywords=keywords,
        limit=4,
        k=60
    )
    

# @router.post("/", response_model=Keywords)
# def get_keywords(
#     query: Query,
# ) -> str:
#     """
#     Return keywords from given query

#     :param query: Query from user.
#     :return: Keywords from query.
#     """
#     return search_pipeline.extract_keywords(input=query.query)


# @router.post("/expend", response_model= QueryExpension)
# def get_query_expension(
#     query: Query,
# ) -> str:
#     """
#     Return Reformulated query from given query and the product description

#     :param query: Query from user.
#     :return: Reformulated query and product description.
#     """
#     return search_pipeline.query_expension(input=query.query)

@router.put("/emb")
def get_query_expension(
    query: Query,
)->None:
    """
    Return Reformulated query from given query and the product description

    :param query: Query from user.
    :return: Reformulated query and product description.
    """
    print(search_pipeline.generate_embedding(input=query.query))


