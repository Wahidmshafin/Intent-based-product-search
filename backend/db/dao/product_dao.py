from typing import List, Optional

from fastapi import Depends
from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession

from backend.db.dependencies import get_db_session
from backend.db.models.dummy_model import ProductTable


class ProductDAO:
    """Class for accessing dummy table."""

    def __init__(self, session: AsyncSession = Depends(get_db_session)) -> None:
        self.session = session

    async def add_product(self, new_id:int, category: str, brand: str, description: str, title: str, price: str, spec: str, embedding: list[float]) -> None:
        """
        Add single dummy to session.

        :param name: name of a dummy.
        """
        self.session.add(ProductTable(new_id=new_id, category = category, brand = brand, description = description, title=title, price=price, spec=spec, embedding = embedding))

    async def get_all_products(self, limit: int) -> List[ProductTable]:
        """
        Get all product models with limit/offset pagination.

        :param limit: limit of products.
        :return: stream of products.
        """
        products = await self.session.execute(
            select(ProductTable).limit(limit),
        )
    
        return list(products.scalars().fetchall())
    
    async def get_products_fromID(self, ids:list[int], limit:int)->List[ProductTable]:
        if not ids:
            return []
        products = await self.session.execute(
            select(ProductTable).where(ProductTable.id.in_(ids)).limit(limit=limit)
            )
        return products.scalars().fetchall()

    async def hybrid_search(self, embedding:list[float], keywords:str, limit: int, k:float=60, count:int = 4):
        """
        Perform Hybrid search on pgvector database.
        """
        stmt = text("""
        WITH semantic_search AS (
            SELECT
                id,
                RANK () OVER (ORDER BY embedding <=> :embeddings) AS rank
            FROM product_table
            ORDER BY embedding <=> :embeddings 
            LIMIT :limit
        ),
        keyword_search AS (
            SELECT
                id,
                RANK () OVER (ORDER BY ts_rank_cd(to_tsvector('english', description), query) DESC) AS rank
            FROM
                product_table,
                websearch_to_tsquery('english', :keywords) AS query
            WHERE
                to_tsvector('english', description) @@ query
            ORDER BY ts_rank_cd(to_tsvector('english', description), query) DESC 
            LIMIT :limit
        ),
        combined_results AS (
            SELECT
                COALESCE(semantic_search.id, keyword_search.id) AS id,
                COALESCE(1.0 / (:k + semantic_search.rank), 0.0) +
                COALESCE(1.0 / (:k + keyword_search.rank), 0.0) AS score
            FROM semantic_search
            FULL OUTER JOIN keyword_search ON semantic_search.id = keyword_search.id
        )
        SELECT
            p.id,
            p.title,
            p.category,
            p.brand,           
            p.description
        FROM combined_results cr
        JOIN product_table p ON cr.id = p.id 
        ORDER BY cr.score DESC
        LIMIT :cnt; 
        """)

        products = await self.session.execute(statement=stmt,params={
        "embeddings": str(embedding), # Ensure embedding is passed as a string representation if needed by your driver
        "limit": limit,
        "keywords": keywords,
        "k": k,
        "cnt":count
        })
        return list(products.fetchall())