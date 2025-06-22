# Enhanced Time Zone Converter API

A comprehensive FastAPI-based REST API for converting times between different time zones with advanced features and robust functionality.

## 🚀 Features

### Core Functionality
- **Time Zone Conversion**: Convert times between any valid time zones, including those with slashes (e.g., America/New_York)
- **Batch Operations**: Convert multiple times simultaneously for improved performance
- **Real-time Current Time**: Get current time in any timezone with automatic DST handling
- **Timezone Discovery**: Search and explore available timezones with intelligent filtering

### Advanced Features
- **Timezone Information**: Detailed timezone metadata including UTC offset, DST status, and abbreviations, with correct handling for all timezones
- **Multi-timezone Operations**: Handle multiple timezones in single requests
- **Intelligent Search**: Fuzzy search through timezone names with partial matching
- **Robust Error Handling**: Comprehensive error handling for invalid timezones, datetime formats, and all edge cases
- **Input Validation**: Strong validation for all inputs with helpful error messages
- **Full Path Support**: Endpoints support timezones with slashes using FastAPI's `{timezone:path}`

### Developer Experience
- **Interactive Documentation**: Auto-generated API docs with Swagger UI
- **Type Safety**: Full Pydantic model validation
- **RESTful Design**: Clean, intuitive API endpoints following REST principles
- **Performance Optimized**: Fast response times with efficient timezone calculations
- **Fully Tested**: All endpoints are covered by automated tests and are production-ready

## 📋 Setup

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Local Installation

1. **Clone or download the project files**

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Run the API:**
```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

### Alternative Run Methods
```bash
# Run with custom host and port
uvicorn main:app --host 0.0.0.0 --port 8080

# Run in production mode
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

## 🚀 Elestio Deployment

### Prerequisites
- Elestio account (sign up at [elest.io](https://elest.io))
- Git repository with your code

### Deployment Steps

#### Method 1: Deploy from GitHub (Recommended)

1. **Push your code to GitHub:**
```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/yourusername/timezone-api.git
git push -u origin main
```

2. **Deploy on Elestio:**
   - Go to [elest.io](https://elest.io)
   - Click "Create New App"
   - Select "GitHub" as source
   - Choose your repository
   - Elestio will automatically detect the Docker configuration and deploy it

#### Method 2: Deploy using Docker Compose

1. **Build and run locally:**
```bash
docker-compose up --build
```

2. **Deploy to Elestio:**
   - Upload your project files to Elestio
   - Elestio will use the `docker-compose.yml` file for deployment

### Configuration Files

The project includes the following deployment files:

- **`Dockerfile`**: Container configuration with security best practices
- **`docker-compose.yml`**: Multi-container orchestration
- **`elestio.yml`**: Elestio-specific configuration
- **`.dockerignore`**: Excludes unnecessary files from Docker build

### Environment Variables

Elestio will automatically set the `PORT` environment variable. No additional configuration is needed.

### Post-Deployment

After deployment, Elestio will provide you with:
- **Live URL**: Your API will be available at `https://your-app-name.elestio.app`
- **Custom Domain**: You can add a custom domain in Elestio dashboard
- **Monitoring**: View logs and performance metrics in Elestio dashboard
- **SSL/HTTPS**: Automatic SSL certificates

### Testing Your Deployed API

Once deployed, test your API using the provided URL:

```bash
# Test the root endpoint
curl https://your-app-name.elestio.app/

# Test timezone conversion
curl -X POST "https://your-app-name.elestio.app/convert" \
-H "Content-Type: application/json" \
-d '{
    "datetime": "2023-12-25 12:00:00",
    "source_timezone": "UTC",
    "target_timezone": "America/New_York"
}'
```

### Scaling and Monitoring

- **Auto-scaling**: Elestio automatically scales your application based on traffic
- **Health checks**: The Dockerfile includes health checks for monitoring
- **Logs**: View real-time logs in Elestio dashboard
- **Metrics**: Monitor performance and resource usage
- **Backup**: Automatic backups and disaster recovery

## 🔧 API Endpoints

### 1. Root Endpoint
- **URL:** `/`
- **Method:** `GET`
- **Description:** API overview and endpoint listing
- **Response:** Welcome message with available endpoints

### 2. List All Timezones
- **URL:** `/timezones`
- **Method:** `GET`
- **Description:** Retrieve complete list of all available timezones
- **Use Case:** Populate timezone dropdowns or lists

### 3. Search Timezones
- **URL:** `/timezones/search?q={search_term}`
- **Method:** `GET`
- **Description:** Intelligent timezone search with partial matching
- **Parameters:**
  - `q` (required): Search term (minimum 1 character)
- **Example:** `/timezones/search?q=America`
- **Use Case:** Find timezones by country, city, or region

### 4. Current Time (Single Timezone)
- **URL:** `/current/{timezone}`
- **Method:** `GET`
- **Description:** Get real-time current time in specified timezone
- **Parameters:**
  - `timezone` (path): Valid timezone identifier
- **Example:** `/current/America/New_York`
- **Use Case:** Display current time for a specific location

### 5. Current Time (Multiple Timezones)
- **URL:** `/current?timezones={timezone1},{timezone2},{timezone3}`
- **Method:** `GET`
- **Description:** Get current time across multiple timezones simultaneously
- **Parameters:**
  - `timezones` (query): Comma-separated list of timezone identifiers
- **Example:** `/current?timezones=UTC,America/New_York,Europe/London`
- **Use Case:** World clock displays or multi-location dashboards

### 6. Timezone Information
- **URL:** `/info/{timezone}`
- **Method:** `GET`
- **Description:** Comprehensive timezone metadata and current status
- **Parameters:**
  - `timezone` (path): Valid timezone identifier
- **Example:** `/info/America/New_York`
- **Use Case:** Timezone analysis and debugging

### 7. Single Time Conversion
- **URL:** `/convert`
- **Method:** `POST`
- **Description:** Convert time between two timezones
- **Request Body:**
```json
{
    "datetime": "2023-12-25 12:00:00",
    "source_timezone": "UTC",
    "target_timezone": "America/New_York"
}
```
- **Use Case:** Individual time conversions for scheduling

### 8. Batch Time Conversion
- **URL:** `/convert/batch`
- **Method:** `POST`
- **Description:** Convert multiple times between different timezones in one request
- **Request Body:**
```json
{
    "conversions": [
        {
            "datetime": "2023-12-25 12:00:00",
            "source_timezone": "UTC",
            "target_timezone": "America/New_York"
        },
        {
            "datetime": "2023-12-25 15:00:00",
            "source_timezone": "UTC",
            "target_timezone": "Europe/London"
        }
    ]
}
```
- **Use Case:** Bulk time conversions for event scheduling or data processing

## 🧪 Testing

### Manual Testing with curl

#### 1. Test Basic Endpoints
```bash
# Test root endpoint
curl http://localhost:8000/

# Test timezone listing
curl http://localhost:8000/timezones

# Test timezone search
curl "http://localhost:8000/timezones/search?q=America"
```

#### 2. Test Current Time Endpoints
```bash
# Test single timezone current time
curl http://localhost:8000/current/America/New_York

# Test multiple timezones current time
curl "http://localhost:8000/current?timezones=UTC,America/New_York,Europe/London"
```

#### 3. Test Timezone Information
```bash
# Test timezone info
curl http://localhost:8000/info/America/New_York
```

#### 4. Test Time Conversion
```bash
# Test single conversion
curl -X POST "http://localhost:8000/convert" \
-H "Content-Type: application/json" \
-d '{
    "datetime": "2023-12-25 12:00:00",
    "source_timezone": "UTC",
    "target_timezone": "America/New_York"
}'

# Test batch conversion
curl -X POST "http://localhost:8000/convert/batch" \
-H "Content-Type: application/json" \
-d '{
    "conversions": [
        {
            "datetime": "2023-12-25 12:00:00",
            "source_timezone": "UTC",
            "target_timezone": "America/New_York"
        },
        {
            "datetime": "2023-12-25 15:00:00",
            "source_timezone": "UTC",
            "target_timezone": "Europe/London"
        }
    ]
}'
```

### Automated Testing

Create a test file `test_api.py`:

```python
import requests
import json

BASE_URL = "http://localhost:8000"

def test_root_endpoint():
    response = requests.get(f"{BASE_URL}/")
    assert response.status_code == 200
    print("✅ Root endpoint test passed")

def test_timezones_endpoint():
    response = requests.get(f"{BASE_URL}/timezones")
    assert response.status_code == 200
    assert "timezones" in response.json()
    print("✅ Timezones endpoint test passed")

def test_search_endpoint():
    response = requests.get(f"{BASE_URL}/timezones/search?q=America")
    assert response.status_code == 200
    data = response.json()
    assert "results" in data
    assert "count" in data
    print("✅ Search endpoint test passed")

def test_current_time_single():
    response = requests.get(f"{BASE_URL}/current/America/New_York")
    assert response.status_code == 200
    data = response.json()
    assert "current_time" in data
    assert "timezone" in data
    print("✅ Current time single test passed")

def test_current_time_multiple():
    response = requests.get(f"{BASE_URL}/current?timezones=UTC,America/New_York")
    assert response.status_code == 200
    data = response.json()
    assert "results" in data
    print("✅ Current time multiple test passed")

def test_timezone_info():
    response = requests.get(f"{BASE_URL}/info/America/New_York")
    assert response.status_code == 200
    data = response.json()
    assert "utc_offset" in data
    assert "is_dst" in data
    print("✅ Timezone info test passed")

def test_single_conversion():
    payload = {
        "datetime": "2023-12-25 12:00:00",
        "source_timezone": "UTC",
        "target_timezone": "America/New_York"
    }
    response = requests.post(f"{BASE_URL}/convert", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "converted_time" in data
    print("✅ Single conversion test passed")

def test_batch_conversion():
    payload = {
        "conversions": [
            {
                "datetime": "2023-12-25 12:00:00",
                "source_timezone": "UTC",
                "target_timezone": "America/New_York"
            },
            {
                "datetime": "2023-12-25 15:00:00",
                "source_timezone": "UTC",
                "target_timezone": "Europe/London"
            }
        ]
    }
    response = requests.post(f"{BASE_URL}/convert/batch", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "results" in data
    print("✅ Batch conversion test passed")

def test_error_handling():
    # Test invalid timezone
    response = requests.get(f"{BASE_URL}/current/Invalid/Timezone")
    assert response.status_code == 400
    print("✅ Error handling test passed")

if __name__ == "__main__":
    print("🧪 Running API tests...")
    test_root_endpoint()
    test_timezones_endpoint()
    test_search_endpoint()
    test_current_time_single()
    test_current_time_multiple()
    test_timezone_info()
    test_single_conversion()
    test_batch_conversion()
    test_error_handling()
    print("🎉 All tests passed!")
```

Run the tests:
```bash
python test_api.py
```

### Performance Testing

Test API performance with multiple concurrent requests:

```bash
# Install Apache Bench (if available)
# On Ubuntu/Debian: sudo apt-get install apache2-utils
# On macOS: brew install httpd

# Test performance
ab -n 100 -c 10 http://localhost:8000/timezones
```

## 📊 Response Examples

### Current Time Response:
```json
{
    "timezone": "America/New_York",
    "current_time": "2023-12-25 07:00:00 EST",
    "utc_offset": "-0500",
    "is_dst": false
}
```

### Timezone Info Response:
```json
{
    "timezone": "America/New_York",
    "current_time": "2023-12-25 07:00:00 EST",
    "utc_offset": "-05:00",
    "is_dst": false,
    "dst_name": "EST"
}
```

### Search Response:
```json
{
    "search_term": "America",
    "results": [
        "America/Adak",
        "America/Anchorage",
        "America/New_York",
        "America/Chicago",
        "America/Denver",
        "America/Los_Angeles"
    ],
    "count": 45
}
```

### Conversion Response:
```json
{
    "source_time": "2023-12-25 12:00:00 UTC",
    "source_timezone": "UTC",
    "converted_time": "2023-12-25 07:00:00 EST",
    "target_timezone": "America/New_York"
}
```

## 🔍 Error Handling

The API includes comprehensive error handling:

### Common Error Scenarios
- **Invalid timezone names**: Returns 400 with descriptive error message
- **Invalid datetime formats**: Returns 400 with format guidance
- **Missing required parameters**: Returns 400 with parameter details
- **Server errors**: Returns 500 with error information

### Error Response Format
```json
{
    "detail": "Invalid timezone: Invalid/Timezone"
}
```

## 📚 Documentation

Once the API is running, access:
- **Interactive API documentation**: `http://localhost:8000/docs`
- **Alternative documentation**: `http://localhost:8000/redoc`
- **OpenAPI specification**: `http://localhost:8000/openapi.json`

## 🚀 Production Deployment

### Elestio Deployment
```bash
# Build Docker image
docker build -t timezone-api .

# Run with Docker Compose
docker-compose up --build
```

### Docker Deployment
```bash
# Build Docker image
docker build -t timezone-api .

# Run container
docker run -p 8000:8000 timezone-api
```

### Traditional Server Deployment
```bash
# Install production dependencies
pip install gunicorn

# Run with Gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new features
5. Submit a pull request

## 📄 License

This project is open source and available under the MIT License. 