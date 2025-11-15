# Nissan Scraper API

A FastAPI-based web scraper application for extracting Nissan vehicle data.

## Project Structure

```
nissan-scraper/
├── app/
│   ├── __init__.py
│   ├── api/          # API routes and endpoints
│   │   └── __init__.py
│   ├── core/         # Core configuration (settings, database, security)
│   │   └── __init__.py
│   ├── models/       # Database models (SQLAlchemy or other ORM)
│   │   └── __init__.py
│   ├── schemas/      # Pydantic schemas for request/response validation
│   │   └── __init__.py
│   ├── services/     # Business logic and scraper implementation
│   │   └── __init__.py
│   └── utils/        # Utility functions and helpers
│       └── __init__.py
├── tests/            # Test files
│   └── __init__.py
├── Dockerfile        # Docker container configuration
├── docker-compose.yml # Docker Compose orchestration
├── .gitignore        # Git ignore patterns
├── env.example       # Example environment variables
├── requirements.txt  # Python dependencies
└── README.md         # This file
```

## Folder Descriptions

### `app/api/`

Contains all API route handlers and endpoint definitions. Organize your routes by feature or resource (e.g., `vehicles.py`, `search.py`).

### `app/core/`

Houses core application configuration including:

- Application settings and environment variables
- Database configuration
- Security and authentication setup
- Logging configuration

### `app/models/`

Database models if you're storing scraped data. Uses SQLAlchemy or another ORM to define data structures.

### `app/schemas/`

Pydantic models for request/response validation and serialization. Ensures data integrity and provides automatic API documentation.

### `app/services/`

Business logic layer containing:

- Web scraping implementation
- Data processing functions
- External service integrations
- Core application logic

### `app/utils/`

Utility functions and helper modules used across the application (e.g., date formatting, data validators, custom exceptions).

### `tests/`

Unit tests, integration tests, and end-to-end tests for your application.

## Installation

1. Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Running the Development Server

```bash
uvicorn app.main:app --reload
```

Or with custom host and port:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

### Available Endpoints

Once running, you can access:

- **Root**: `http://localhost:8000/` - API info
- **Health Check**: `http://localhost:8000/health` - Service health status
- **Swagger UI**: `http://localhost:8000/docs` - Interactive API documentation
- **ReDoc**: `http://localhost:8000/redoc` - Alternative API documentation

### API Endpoints

**Health:**

- `GET /health` - Health check
- `GET /ping` - Simple ping/pong

**Vehicles:**

- `GET /api/v1/vehicles` - List all vehicles (with filters)
- `GET /api/v1/vehicles/{id}` - Get specific vehicle
- `POST /api/v1/scrape` - Scrape vehicle from URL
- `GET /api/v1/models` - List available models

### Testing the API

Using curl:

```bash
# Health check
curl http://localhost:8000/health

# Get vehicles
curl http://localhost:8000/api/v1/vehicles

# Get vehicles with filters
curl "http://localhost:8000/api/v1/vehicles?model=Altima&year=2024&limit=5"

# Scrape a vehicle
curl -X POST http://localhost:8000/api/v1/scrape \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.nissan.com/vehicles/altima", "include_specs": true}'
```

Or use the interactive Swagger UI at `http://localhost:8000/docs`

## Development

### How to Add Routers

Routers in FastAPI help organize your endpoints. Here's how to add a new router:

#### Step 1: Create a Router File

Create a new file in `app/api/`, for example `app/api/dealers.py`:

```python
from fastapi import APIRouter, HTTPException
from typing import List

router = APIRouter()

@router.get("/dealers")
async def get_dealers():
    """Get list of Nissan dealers"""
    return {
        "success": True,
        "data": ["Dealer 1", "Dealer 2"]
    }

@router.get("/dealers/{dealer_id}")
async def get_dealer(dealer_id: str):
    """Get specific dealer details"""
    return {
        "success": True,
        "data": {"id": dealer_id, "name": "Dealer Name"}
    }
```

#### Step 2: Register the Router

Add it to `app/main.py`:

```python
from app.api import dealers  # Import your new router

# Include the router
app.include_router(
    dealers.router,
    prefix="/api/v1",
    tags=["Dealers"]
)
```

#### Step 3: Define Schemas (Optional)

Create Pydantic schemas in `app/schemas/dealer.py`:

```python
from pydantic import BaseModel

class Dealer(BaseModel):
    id: str
    name: str
    address: str
    phone: str
```

#### Step 4: Implement Service Logic

Create business logic in `app/services/dealer_service.py`:

```python
class DealerService:
    async def get_dealers(self):
        # Your scraping/business logic here
        pass
```

### Example: Complete Router Implementation

Here's what's already set up in the project:

**Main App** (`app/main.py`):

```python
from fastapi import FastAPI
from app.api import health, scraper

app = FastAPI(title="Nissan Scraper API")

# Register routers
app.include_router(health.router, tags=["Health"])
app.include_router(scraper.router, prefix="/api/v1", tags=["Scraper"])
```

**Router** (`app/api/scraper.py`):

- `GET /api/v1/vehicles` - List vehicles
- `POST /api/v1/scrape` - Scrape vehicle data
- `GET /api/v1/vehicles/{vehicle_id}` - Get specific vehicle
- `GET /api/v1/models` - List available models

**Schemas** (`app/schemas/vehicle.py`):

- `VehicleRequest` - For POST requests
- `VehicleResponse` - For responses

**Service** (`app/services/scraper_service.py`):

- Contains the actual scraping logic

### Running Tests

```bash
pytest
```

## Production Deployment

### Method 1: Using Gunicorn with Uvicorn Workers (Recommended)

This is the recommended approach for production deployments on Linux servers.

1. Install Gunicorn (already in requirements.txt):

```bash
pip install gunicorn
```

2. Run with Gunicorn:

```bash
gunicorn app.main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000 \
  --timeout 120 \
  --access-logfile - \
  --error-logfile -
```

**Worker count formula:** `(2 x CPU_cores) + 1`

### Method 2: Using Docker

1. Create a `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app ./app

EXPOSE 8000

CMD ["gunicorn", "app.main:app", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]
```

2. Create a `docker-compose.yml`:

```yaml
version: "3.8"

services:
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      - ENV=production
    restart: unless-stopped
```

3. Build and run:

```bash
docker-compose up -d
```

### Method 3: Using Systemd Service (Linux)

1. Create a service file `/etc/systemd/system/nissan-scraper.service`:

```ini
[Unit]
Description=Nissan Scraper API
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/nissan-scraper
Environment="PATH=/var/www/nissan-scraper/venv/bin"
ExecStart=/var/www/nissan-scraper/venv/bin/gunicorn \
  app.main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000

[Install]
WantedBy=multi-user.target
```

2. Enable and start the service:

```bash
sudo systemctl daemon-reload
sudo systemctl enable nissan-scraper
sudo systemctl start nissan-scraper
sudo systemctl status nissan-scraper
```

### Method 4: With Nginx Reverse Proxy

1. Install and configure Nginx `/etc/nginx/sites-available/nissan-scraper`:

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # Timeout settings for scraping
        proxy_connect_timeout 300s;
        proxy_send_timeout 300s;
        proxy_read_timeout 300s;
    }
}
```

2. Enable the site:

```bash
sudo ln -s /etc/nginx/sites-available/nissan-scraper /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### Environment Variables for Production

Create a `.env` file (never commit this to git):

```bash
ENV=production
DEBUG=False
HOST=0.0.0.0
PORT=8000
WORKERS=4
LOG_LEVEL=info
```

### Performance Tuning

1. **Worker count**: Adjust based on CPU cores and workload
2. **Timeout**: Increase for long-running scrape operations
3. **Connection pooling**: Use for database connections
4. **Rate limiting**: Implement to prevent abuse
5. **Caching**: Use Redis for frequently accessed data

### Monitoring and Logging

Consider adding:

- **Application monitoring**: New Relic, DataDog, or Prometheus
- **Error tracking**: Sentry
- **Logging**: ELK Stack or CloudWatch
- **Uptime monitoring**: UptimeRobot or Pingdom

### Security Checklist

- [ ] Use HTTPS (Let's Encrypt for free SSL)
- [ ] Set up firewall (UFW or iptables)
- [ ] Keep dependencies updated
- [ ] Use environment variables for secrets
- [ ] Implement rate limiting
- [ ] Enable CORS properly
- [ ] Use authentication for sensitive endpoints
- [ ] Regular backups if using a database

### Cloud Deployment Options

**AWS:**

```bash
# Deploy to EC2, ECS, or Elastic Beanstalk
eb init -p python-3.11 nissan-scraper
eb create production-env
```

**Heroku:**

```bash
heroku create nissan-scraper-api
git push heroku main
```

**Railway/Render:** Connect your GitHub repo and deploy automatically.

## License

MIT
