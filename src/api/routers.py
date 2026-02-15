from fastapi import APIRouter

from src.api.places import router as places_router
from src.api.projects import router as projects_router

router = APIRouter()
router.include_router(projects_router, prefix="/projects", tags=["Projects"])
router.include_router(places_router, prefix="/projects", tags=["Places"])
