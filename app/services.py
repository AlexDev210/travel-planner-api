import httpx
from fastapi import HTTPException

async def verify_place_exists(external_id: int):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"https://api.artic.edu/api/v1/artworks/{external_id}")
        if response.status_code != 200:
            raise HTTPException(status_code=400, detail=f"Place {external_id} not found in Art Institute API.")
