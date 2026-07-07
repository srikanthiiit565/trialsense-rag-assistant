"""API routes for the TrialSense assistant."""
from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
async def health_check():
    return {
        "status": "healthy"
    }


@router.get("/version")
async def version():
    return {
        "version": "1.0.0"
    }


@router.get("/ping")
async def ping():
    return {
        "message": "pong"
    }