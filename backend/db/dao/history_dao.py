from typing import List, Optional

from fastapi import Depends
from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import NoResultFound

from backend.db.dependencies import get_db_session
from backend.db.models.dummy_model import HistoryTable


class HistoryDAO:
    """Class for accessing dummy table."""

    def __init__(self, session: AsyncSession = Depends(get_db_session)) -> None:
        self.session = session

    async def add_history(self,query: str, result: list[int], feedback:int) -> None:
        """
        Add single dummy to session.

        :param name: name of a dummy.
        """
        self.session.add(HistoryTable(query=query, result = result, feedback = feedback))

    async def update_feedback(self, history_id: int, new_feedback: int) -> None:
        """
        Update the feedback value for a HistoryTable entry by its ID.

        :param history_id: the primary key of the HistoryTable row to update
        :param new_feedback: the new feedback value to set
        """
        # 1. Fetch the existing history row
        stmt = select(HistoryTable).where(HistoryTable.id == history_id)
        result = await self.session.execute(stmt)
        history_obj = result.scalar_one_or_none()

        if history_obj is None:
            raise NoResultFound(f"No HistoryTable entry found with id={history_id}")

        # 2. Update the feedback field
        history_obj.feedback = new_feedback

        # 3. Commit the change
        await self.session.commit()

    async def get_all_history(self, limit: int) -> List[HistoryTable]:
        """
        Get all product models with limit/offset pagination.

        :param limit: limit of products.
        :return: stream of products.
        """
        history = await self.session.execute(
            select(HistoryTable).limit(limit)
        )

        return list(history.scalars().fetchall())
    