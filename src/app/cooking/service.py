import logging

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.misc.dependencies import get_async_session

logger = logging.getLogger(__name__)


class CookingService:
    def __init__(self,
                 db: AsyncSession = Depends(get_async_session)):
        self.db = db
