from fastapi import APIRouter
from datetime import datetime

router = APIRouter()


@router.get("/health")
async def health_check():
    """
    Health check endpoint for monitoring and load balancers
    """
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "Nissan Scraper API",
    }


@router.get("/ping")
async def ping():
    """
    Simple ping endpoint
    """
    return {"message": "pong"}

