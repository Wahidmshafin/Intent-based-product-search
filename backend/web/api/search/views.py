from typing import List
import json

from fastapi import APIRouter
from fastapi.param_functions import Depends

from backend.db.dao.product_dao import ProductDAO
from backend.db.dao.history_dao import HistoryDAO
from backend.web.api.search.schema import Keywords, Query, QueryExpension, Vectors, Historys
from backend.web.api.search.rag import SearchPipeline
from backend.settings import settings

router = APIRouter()
search_pipeline = SearchPipeline()
history_dao = HistoryDAO()

@router.post("/", response_model=List[Vectors])
async def hybrid_search(
    query: Query,
    product_dao: ProductDAO = Depends(),
    history_dao: HistoryDAO = Depends()
) -> List[Vectors]:
    """
    Return keywords from given query

    :param query: Query from user.
    :return: Keywords from query.
    """
    # keywords = search_pipeline.extract_keywords(query)
    # keywords = ["Big", "Shoes"]

    # better_query = search_pipeline.query_expension(query)

    # better_query = """
    # expended_query: "medium men's sports sneakers
    # product_title: Men's Medium Sports Shoes,
    # product_detail: • Breathable mesh upper for all-day comfort\n• Lightweight cushioned sole for added durability and flexibility\n• Durable rubber outsole for traction on various surfaces\n• Made from breathable, moisture-wicking fabric to keep feet dry\n• Ideal for running, casual wear, and sports activities\n• Available in black, white, and navy colors
    # """
    
    ner = search_pipeline.generate_test_rag(query)["content"]
    print(ner)

    embedding = search_pipeline.generate_embedding(ner)
    keywords = ""
    ner_dict = json.loads(ner)
    for key, value in ner_dict.items():
        keywords = keywords + " "+ str(value)
    # print(embedding)
    response = await product_dao.hybrid_search(
        embedding=embedding,
        keywords=keywords,
        limit=10,
        k=60,
        count=5
    )
    ids = []
    for res in response:
        ids.append(res.id)
    await history_dao.add_history(query=query.query,result=ids, feedback=0)
    return response


@router.post("/history", response_model=List[Historys])
async def get_history(
    limit:int,
    history_dao: HistoryDAO = Depends()
)->List[Historys]:
    """
    """
    return await history_dao.get_all_history(limit=limit)

@router.put("/feedback")
async def get_history(
    id:int,
    feedback: int,
    history_dao: HistoryDAO = Depends()
):
    """
    """
    return await history_dao.update_feedback(id,feedback)

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


