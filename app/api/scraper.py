from fastapi import APIRouter, HTTPException
from app.schemas.vehicle import VehicleRequest
from app.services.scraper_service import ScraperService

router = APIRouter()
scraper_service = ScraperService()


@router.post("/scrape-vehicle-data")
async def scrape_vehicle(request: VehicleRequest):
    """
    Scrape data for a specific Nissan vehicle
    
    - **url**: URL of the vehicle page to scrape
    """
    try:
        result = await scraper_service.scrape_vehicle_data(
            url=request.url
        )
        return {
            "success": True,
            "data": result,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))