from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.session import get_db
from src.services.db_service import DBService


def get_db_service(db: AsyncSession = Depends(get_db)) -> DBService:
    return DBService(db)
