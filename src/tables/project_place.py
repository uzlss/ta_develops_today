from sqlalchemy import Boolean, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.base import Base
from src.tables.mixins import TimeMixin


class ProjectPlace(Base, TimeMixin):
    __table_args__ = (
        UniqueConstraint(
            "project_id", "external_id", name="uq_project_external_place"
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    project_id: Mapped[int] = mapped_column(
        ForeignKey("projects.id", ondelete="CASCADE"), nullable=False
    )
    external_id: Mapped[int] = mapped_column(Integer, nullable=False)
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    artist: Mapped[str | None] = mapped_column(String(500), nullable=True)
    notes: Mapped[str | None] = mapped_column(String, nullable=True)
    visited: Mapped[bool] = mapped_column(
        Boolean, default=False, server_default="false"
    )

    project: Mapped["Project"] = relationship(back_populates="places")
