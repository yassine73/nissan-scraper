from pydantic import BaseModel, HttpUrl, Field


class VehicleRequest(BaseModel):
    """Request schema for scraping vehicle data"""
    url: HttpUrl = Field(..., description="URL of the vehicle page to scrape")

    class Config:
        json_schema_extra = {
            "example": {
                "url": "https://www.example-url.com/list-of-vehicles",
            }
        }


class VehicleData(BaseModel):
    """Response schema for vehicle data"""
    model_designation: str = Field(..., description="Model designation")
    year: str = Field(..., description="Year")
    region: str = Field(..., description="Region")
    steering: str = Field(..., description="Steering")
    transmission_type: str = Field(..., description="Transmission type")
    series: str = Field(..., description="Series")
    engine: str = Field(..., description="Engine")
    class_: str = Field(..., description="Class")
    body: str = Field(..., description="Body")
    additional_body: str = Field(..., description="Additional body")
    additional_engine: str = Field(..., description="Additional engine")
    additional_area: str = Field(..., description="Additional area")
    additional_grade: str = Field(..., description="Additional grade")
    additional_transmission: str = Field(..., description="Additional transmission")

    class Config:
        json_schema_extra = {
            "example": {
                "model_designation": "100nx b13",
                "year": "1994",
                "region": "Europe",
                "steering": "Right hand",
                "transmission_type": "Automatic",
                "series": "B13",
                "engine": "GA16DE TYPE ENGINE",
                "class_": "TYPE A GRADE",
                "body": "COUPE T/BAR",
                "additional_body": "COUPE T/BAR(C/T)",
                "additional_engine": "GA16DE TYPE ENGINE(GA16DE)",
                "additional_area": "EUR/A(EUR/A)",
                "additional_grade": "TYPE A GRADE(T/A)",
                "additional_transmission": "AUTOMATIC TRANSMISSION(AT)",
            }
        }

