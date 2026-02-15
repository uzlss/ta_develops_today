import datetime

from pydantic import BaseModel, Field

from src.schemas.place import PlaceInProjectCreate, PlaceResponse


# --- Request ---


class ProjectCreate(BaseModel):
    """Create a new travel project."""

    name: str = Field(min_length=1, max_length=255)
    description: str | None = None
    start_date: datetime.date | None = None
    places: list[PlaceInProjectCreate] = Field(min_length=1, max_length=10)


class ProjectUpdate(BaseModel):
    """Update travel project info."""

    name: str | None = Field(None, min_length=1, max_length=255)
    description: str | None = None
    start_date: datetime.date | None = None


# --- Response ---


class ProjectResponse(BaseModel):
    """Full project with places."""

    id: int
    name: str
    description: str | None
    start_date: datetime.date | None
    is_completed: bool
    places: list[PlaceResponse]
    created_at: datetime.datetime

    model_config = {"from_attributes": True}


class ProjectListResponse(BaseModel):
    """Project summary for list endpoint."""

    id: int
    name: str
    description: str | None
    start_date: datetime.date | None
    is_completed: bool
    places_count: int
    created_at: datetime.datetime

    model_config = {"from_attributes": True}
