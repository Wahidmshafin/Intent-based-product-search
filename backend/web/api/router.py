from fastapi.routing import APIRouter

from backend.web.api import docs, monitoring, redis, search, productTable

api_router = APIRouter()
api_router.include_router(monitoring.router)
api_router.include_router(docs.router)
api_router.include_router(search.router, prefix="/search", tags=["search"])
api_router.include_router(productTable.router, prefix="/product", tags=["product"])
api_router.include_router(redis.router, prefix="/redis", tags=["redis"])
