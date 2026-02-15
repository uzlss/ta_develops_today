from fastapi import APIRouter, Depends, HTTPException, Query, status

from src.dependencies import get_db_service
from src.schemas.pagination import PaginatedResponse
from src.schemas.place import PlaceResponse
from src.schemas.project import (
    ProjectCreate,
    ProjectListResponse,
    ProjectResponse,
    ProjectUpdate,
)
from src.services.artic_service import ArticService
from src.services.db_service import DBService

router = APIRouter()


@router.post("/", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
async def create_project(
    body: ProjectCreate,
    svc: DBService = Depends(get_db_service),
):
    """Create a travel project with places."""
    places_data = []
    seen_ids: set[int] = set()
    for p in body.places:
        if p.external_id in seen_ids:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Duplicate external_id {p.external_id} in request",
            )
        seen_ids.add(p.external_id)

        artwork = await ArticService.validate_artwork(p.external_id)
        places_data.append(
            {
                "external_id": artwork["id"],
                "title": artwork["title"],
                "artist": artwork.get("artist_display"),
            }
        )

    project = await svc.create_project(
        name=body.name,
        description=body.description,
        start_date=body.start_date,
        places_data=places_data,
    )
    return project


@router.get("/", response_model=PaginatedResponse[ProjectListResponse])
async def list_projects(
    offset: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    svc: DBService = Depends(get_db_service),
):
    """List all travel projects with pagination."""
    items = await svc.get_projects(offset=offset, limit=limit)
    total = await svc.count_projects()
    return PaginatedResponse(items=items, total=total, offset=offset, limit=limit)


@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(
    project_id: int,
    svc: DBService = Depends(get_db_service),
):
    """Get a single travel project with its places."""
    project = await svc.get_project(project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Project not found"
        )
    return project


@router.put("/{project_id}", response_model=ProjectResponse)
async def update_project(
    project_id: int,
    body: ProjectUpdate,
    svc: DBService = Depends(get_db_service),
):
    """Update project info (name, description, start_date)."""
    project = await svc.get_project(project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Project not found"
        )

    update_data = body.model_dump(exclude_unset=True)
    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No fields to update",
        )

    project = await svc.update_project(project, update_data)
    return project


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(
    project_id: int,
    svc: DBService = Depends(get_db_service),
):
    """Delete a project. Blocked if any place is already visited."""
    project = await svc.get_project(project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Project not found"
        )

    if any(p.visited for p in project.places):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Cannot delete project with visited places",
        )

    await svc.delete_project(project)
