import re
from typing import Any

from sqlalchemy.orm import DeclarativeBase, declared_attr
"""
Based on https://github.com/tiangolo/full-stack-fastapi-postgresql/
"""


def camel_to_snake(name: str) -> str:
    """Convert CamelCase to snake_case."""
    s = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1_\2", name)
    return re.sub(r"([a-z\d])([A-Z])", r"\1_\2", s).lower()


class Base(DeclarativeBase):
    """Base class with auto-generated __tablename__."""

    id: Any
    __name__: str

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return camel_to_snake(cls.__name__) + "s"
