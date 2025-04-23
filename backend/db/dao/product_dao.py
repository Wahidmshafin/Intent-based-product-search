from typing import List, Optional

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.db.dependencies import get_db_session
from backend.db.models.dummy_model import ProductTable


class ProductDAO:
    """Class for accessing dummy table."""

    def __init__(self, session: AsyncSession = Depends(get_db_session)) -> None:
        self.session = session

    async def add_product(self, colorname: str, description: str, name: str, fulldescription: str, embedding: list[str]) -> None:
        """
        Add single dummy to session.

        :param name: name of a dummy.
        """
        self.session.add(ProductTable(colorname=colorname, description = description, name = name, fulldescription = fulldescription, embedding = embedding))

    async def get_all_dummies(self, limit: int, offset: int) -> List[ProductTable]:
        """
        Get all dummy models with limit/offset pagination.

        :param limit: limit of dummies.
        :param offset: offset of dummies.
        :return: stream of dummies.
        """
        raw_dummies = await self.session.execute(
            select(ProductTable).limit(limit).offset(offset),
        )

        return list(raw_dummies.scalars().fetchall())
