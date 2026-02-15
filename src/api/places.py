from fastapi import APIRouter, Depends, HTTPException, status

from src.dependencies import get_db_service
from src.schemas.place import PlaceAdd, PlaceResponse, PlaceUpdate
from src.services.artic_service import ArticService
from src.services.db_service import DBService

router = APIRouter()


@router.post(
    "/{project_id}/places",
    response_model=PlaceResponse,
    status_code=status.HTTP_201_CREATED,
)
async def add_place(
    project_id: int,
    body: PlaceAdd,
    svc: DBService = Depends(get_db_service),
):
    """Add a place to an existing project."""
    project = await svc.get_project(project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Project not found"
        )

    if await svc.count_places(project_id) >= 10:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A project can have at most 10 places",
        )

    if await svc.place_exists(project_id, body.external_id):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Place {body.external_id} already exists in this project",
        )

    artwork = await ArticService.validate_artwork(body.external_id)

    place = await svc.add_place(
        project_id,
        {
            "external_id": artwork["id"],
            "title": artwork["title"],
            "artist": artwork.get("artist_display"),
        },
    )
    return place


@router.get("/{project_id}/places", response_model=list[PlaceResponse])
async def list_places(
    project_id: int,
    svc: DBService = Depends(get_db_service),
):
    """List all places for a project."""
    project = await svc.get_project(project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Project not found"
        )
    return await svc.get_places(project_id)


@router.get(
    "/{project_id}/places/{place_id}", response_model=PlaceResponse
)
async def get_place(
    project_id: int,
    place_id: int,
    svc: DBService = Depends(get_db_service),
):
    """Get a single place within a project."""
    place = await svc.get_place(project_id, place_id)
    if not place:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Place not found"
        )
    return place


@router.patch(
    "/{project_id}/places/{place_id}", response_model=PlaceResponse
)
async def update_place(
    project_id: int,
    place_id: int,
    body: PlaceUpdate,
    svc: DBService = Depends(get_db_service),
):
    """Update a place's notes or mark it as visited."""
    place = await svc.get_place(project_id, place_id)
    if not place:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Place not found"
        )

    update_data = body.model_dump(exclude_unset=True)
    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No fields to update",
        )

    place = await svc.update_place(place, update_data)
    return place
