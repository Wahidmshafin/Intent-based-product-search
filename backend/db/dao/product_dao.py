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

    async def add_product(self, colorname: str, description: str, name: str, fulldescription: str, embedding: list[float]) -> None:
        """
        Add single dummy to session.

        :param name: name of a dummy.
        """
        self.session.add(ProductTable(colorname=colorname, description = description, name = name, fulldescription = fulldescription, embedding = embedding))

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
    
    async def hybrid_search(self, embedding:list[float], keywords:list[str], limit: int, k:float=60, count:int = 10):
        """
        Perform Hybrid search on pgvector database.
        """
        stmt = text("""
        WITH semantic_search AS (
            SELECT
                id,
                -- Calculate semantic rank
                RANK () OVER (ORDER BY embedding <=> :embeddings) AS rank
            FROM product_table
            ORDER BY embedding <=> :embeddings -- Order by for LIMIT
            LIMIT :limit
        ),
        keyword_search AS (
            SELECT
                id,
                -- Calculate keyword rank
                RANK () OVER (ORDER BY ts_rank_cd(to_tsvector('english', fulldescription), query) DESC) AS rank
            FROM
                product_table,
                to_tsquery('english',array_to_string(:keywords, ' | ')) query
            WHERE
                to_tsvector('english', fulldescription) @@ query -- Optional but recommended filter
            ORDER BY ts_rank_cd(to_tsvector('english', fulldescription), query) DESC -- Order by for LIMIT
            LIMIT :limit
        ),
        -- Combine results from both searches and calculate the hybrid score
        combined_results AS (
            SELECT
                COALESCE(semantic_search.id, keyword_search.id) AS id,
                COALESCE(1.0 / (:k + semantic_search.rank), 0.0) +
                COALESCE(1.0 / (:k + keyword_search.rank), 0.0) AS score
            FROM semantic_search
            FULL OUTER JOIN keyword_search ON semantic_search.id = keyword_search.id
        )
        -- Final select: Join combined results with product_table to get name and fulldescription
        SELECT
            p.id,
            p.name,           -- Added name
            p.fulldescription,-- Added fulldescription
        FROM combined_results cr
        JOIN product_table p ON cr.id = p.id -- Join back to get other columns
        ORDER BY cr.score DESC
        LIMIT :count; -- Apply final limit based on hybrid score
        """)

        products = await self.session.execute(statement=stmt,params={
        "embeddings": str(embedding), # Ensure embedding is passed as a string representation if needed by your driver
        "keywords": keywords,
        "limit": limit,
        "k": k
        })
        return list(products.fetchall())