from typing import List
import json

from fastapi import APIRouter
from fastapi.param_functions import Depends
from redis.asyncio import ConnectionPool, Redis

from backend.db.dao.product_dao import ProductDAO
from backend.web.api.search.schema import Query, Vectors
from backend.web.api.search.rag import SearchPipeline
from backend.services.redis.dependency import get_redis_pool

router = APIRouter()
search_pipeline = SearchPipeline()


@router.post("/", response_model=List[Vectors])
async def hybrid_search(
    query: Query,
    product_dao: ProductDAO = Depends(),
    redis_pool: ConnectionPool = Depends(get_redis_pool),
) -> List[Vectors]:
    """
    Return keywords from given query

    First checks if the query results exist in Redis cache.
    If found, returns cached product IDs.
    If not, performs search operations and saves result to Redis.

    :param query: Query from user.
    :param product_dao: DAO for product database operations.
    :param redis_pool: redis connection pool.
    :return: Keywords from query.
    """
    # Create a unique key for this query
    cache_key = f"search:{query.query}"

    # Check if results exist in Redis
    async with Redis(connection_pool=redis_pool) as redis:
        cached_results = await redis.get(cache_key)
        
        if cached_results:
            # Return cached results if found
            return json.loads(cached_results.decode('utf-8'))
    
    # If not in cache, perform the search operation
    print(f"Query: {query.query}")
    print(f"Cache key: {cache_key}")
    ner = search_pipeline.generate_test_rag(query)["content"]
    print(ner)

    embedding = search_pipeline.generate_embedding(ner)
    keywords = ""
    ner_dict = json.loads(ner)
    for key, value in ner_dict.items():
        keywords = keywords + " " + str(value)
    
    # Get search results
    results = await product_dao.hybrid_search(
        embedding=embedding,
        keywords=keywords,
        limit=10,
        k=60,
        count=5
    )
    
    # Cache the results in Redis
    async with Redis(connection_pool=redis_pool) as redis:
        # Convert the results to JSON string and save to Redis
        # We need to convert the results to a dict first
        serializable_results = [
            {
                "id": result.id,
                "title": result.title,
                "category": result.category,
                "brand": result.brand,
                "description": result.description
            }
            for result in results
        ]
        await redis.set(
            cache_key, 
            json.dumps(serializable_results),
            ex=3600  # Expire after 1 hour
        )
    
    return results
    

@router.put("/emb")
def get_query_expension(
    query: Query,
) -> None:
    """
    Return Reformulated query from given query and the product description

    :param query: Query from user.
    :return: Reformulated query and product description.
    """
    print(search_pipeline.generate_embedding(input=query.query))


