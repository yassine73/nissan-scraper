from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import scraper, health

# Create FastAPI app instance
app = FastAPI(
    title="Nissan Scraper API",
    description="API for scraping Nissan vehicle data",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router, tags=["Health"])
app.include_router(scraper.router, prefix="/api/v1", tags=["Scraper"])

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "Welcome to Nissan Scraper API",
        "version": "1.0.0",
        "docs": "/docs",
    }

