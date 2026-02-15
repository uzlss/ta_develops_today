import datetime

from pydantic import BaseModel, Field


# --- Place schemas (used inline in project schemas too) ---


class PlaceInProjectCreate(BaseModel):
    """Place to include when creating a project."""

    external_id: int


class PlaceAdd(BaseModel):
    """Add a place to an existing project."""

    external_id: int


class PlaceUpdate(BaseModel):
    """Update a place's notes or visited status."""

    notes: str | None = None
    visited: bool | None = None


class PlaceResponse(BaseModel):
    """Place response."""

    id: int
    external_id: int
    title: str
    artist: str | None
    notes: str | None
    visited: bool
    created_at: datetime.datetime

    model_config = {"from_attributes": True}
