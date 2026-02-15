from fastapi import FastAPI

from src.api.routers import router

app = FastAPI(title="Travel Planner API", version="0.1.0")

app.include_router(router, prefix="/api/v1")


@app.get("/")
async def root():
    return {"message": "Hello world"}
