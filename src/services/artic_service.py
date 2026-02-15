import httpx
from fastapi import HTTPException, status

from src.config import settings


class ArticService:
    """Client for the Art Institute of Chicago API."""

    @staticmethod
    async def get_artwork(artwork_id: int) -> dict | None:
        """Fetch a single artwork by ID. Returns None if not found."""
        async with httpx.AsyncClient() as client:
            resp = await client.get(
                f"{settings.ARTIC_API_BASE_URL}/artworks/{artwork_id}",
                params={"fields": "id,title,artist_display,place_of_origin"},
            )
            if resp.status_code == 200:
                return resp.json()["data"]
            return None

    @staticmethod
    async def validate_artwork(artwork_id: int) -> dict:
        """Validate artwork exists; raise 404 if not found."""
        data = await ArticService.get_artwork(artwork_id)
        if not data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Artwork {artwork_id} not found in Art Institute API",
            )
        return data
