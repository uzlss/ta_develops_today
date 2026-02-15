import datetime

from sqlalchemy import Date, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.base import Base
from src.tables.mixins import TimeMixin


class Project(Base, TimeMixin):

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(String, nullable=True)
    start_date: Mapped[datetime.date | None] = mapped_column(Date, nullable=True)

    places: Mapped[list["ProjectPlace"]] = relationship(
        back_populates="project", cascade="all, delete-orphan"
    )

    @property
    def is_completed(self) -> bool:
        return len(self.places) > 0 and all(p.visited for p in self.places)

    @property
    def places_count(self) -> int:
        return len(self.places)
