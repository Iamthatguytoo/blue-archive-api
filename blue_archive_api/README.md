# Blue Archive API

A FastAPI-based API for querying Blue Archive students (characters) data, gacha calculations, pull simulations, and probability analysis.


## Quick Start

```bash
docker-compose run init_db
docker-compose up -d api
```

Register an API key:

```bash
curl -X POST http://localhost:8000/auth/register
```

or in Windows:

```powershell
Invoke-RestMethod -Method POST -Uri "http://localhost:8000/auth/register"
```

Query students:

```bash
curl -H "x-api-key: YOUR_KEY" \
"http://localhost:8000/students?name=Hina"
```
or in Windows:

```powershell
Invoke-WebRequest `
  -Uri "http://localhost:8000/students?name=Hina" `
  -Headers @{ "x-api-key" = "YOUR_API_KEY" }
```

## Features

- Retrieve student data from MongoDB with filtering and pagination
- Generate and verify API keys for secure access
- Calculate gacha pull probabilities and spark reachability
- Simulate gacha pulls with statistical analysis
- Analyze pull targets for desired students
- Dockerized for easy deployment

## Installation & Setup

### Prerequisites
- Docker and Docker Compose (for containerized setup)
- OR Python 3.11+ and MongoDB (for local setup)
- MongoDB instance running and accessible (local or cloud)

 ### Environment Variables
  Create either:
    - `.env.local` for local development (MongoDB running on localhost)
    - `.env.prod` for production/deployment (MongoDB Atlas or remote database)

  Example `.env.local` (for local MongoDB):
  CLIENT=mongodb://DevUser:DevPass1234@localhost:27017/?authSource=admin
  DATABASE=MyStuff
  API_COLLECTION=blue_archive_students
  API_COLLECTION_KEYS=blue_archive_api_secret_keys

  Example `.env.prod` (for MongoDB Atlas/remote):
  CLIENT=mongodb+srv://<username>:<password>@cluster0.example.mongodb.net/
  DATABASE=blue_archive_api
  API_COLLECTION=blue_archive_students
  API_COLLECTION_KEYS=api_keys

  ⚠️ **Important**: These files contain sensitive credentials and are:
  - Excluded from Docker images via `.dockerignore`
  - Should be added to `.gitignore` to prevent accidental commits
  - Loaded at runtime by Docker Compose, not baked into images

### Using Docker Compose (Recommended)

#### 1. Initialize Database
This step scrapes and loads student data into MongoDB.
Make sure your MongoDB is running and accessible at the connection string specified in secret.env.

```bash
docker-compose run init_db
```

Run this again anytime you want to refresh the dataset.

#### 2. Start the API
```bash
docker-compose up -d api
```

The API will be available at:
http://localhost:8000


### Local Setup
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Ensure MongoDB is running and accessible
3. Set environment variables in `secret.env` (adjust CLIENT for local MongoDB if needed)
4. Run the API:
   ```bash
   uvicorn blue_archive_characters_api:server --host 0.0.0.0 --port 8000
   ```

## API Endpoints

### Authentication
- `POST /auth/register` - Generate a new API key (returns `sk_*` key)

### Student Data
- `GET /students` - Retrieve paginated student data with filtering
  - Query Parameters:
    - `name` (string): Filter by student name (regex prefix match)
    - `base_name` (string): Filter by base name (exact match)
    - `limit` (int, default 20): Number of results per page
    - `skip` (int, default 0): Number of results to skip
    - Plus any fields from the `StudentFilter` model (school, position, damage_type, etc.)

### Gacha Calculations
- `POST /gacha-calculate` - Calculate gacha odds
  - Body: `CalcRequest` (pyroxene: int, rate_up: float)
  - Returns: `CalcResponse` with pulls, spark reachability, and probabilities

### Gacha Simulation
- `POST /gacha-simulate` - Simulate gacha pulls
  - Body: `GachaPullSimulationRequest`
    - simulations: int (1-10000)
    - pyroxene: int
    - rate_up: float (0-1)
    - rate_up_3_star: float (0-1)
    - pity_threshold: int
    - spark_threshold: int
  - Returns: `GachaPullSimulationResponse` with simulation statistics

### Pull Analysis
- `POST /analyze-pulls` - Analyze pull targets
  - Body: `AnalyzePullsRequest` (probability: float, rate_up: float)
  - Returns: `AnalyzePullsResponse` with required pulls, pyroxene needed, confidence, and risk level

## Project Structure
```
blue_archive_api/
├── blue_archive_characters_api.py   # Main FastAPI application
├── models.py                        # Pydantic models
├── requirements.txt                 # Python dependencies
├── Dockerfile                       # Container definition
├── docker-compose.yaml              # Service orchestration
├── secret.env                       # Environment variables (not in repo)
├── auth/                            # Authentication modules
│   ├── create_random_key.py
│   └── key_verification.py
├── db/                              # Database connection
│   └── database.py
├── services/                        # Business logic
│   ├── retrieve_students.py
│   ├── gacha_calculate.py
│   ├── gacha_simulate.py
│   └── analyze_pulls.py
└── get_request_test.py              # Simple test script
```

## Notes
- The API key is only shown once upon generation - store it securely
- All protected endpoints require the `x-api-key` header with a valid key
- The Docker container includes Playwright Chromium (currently unused but available for future web scraping needs)
- Student data must be present in the MongoDB collection for the `/students` endpoint to return results

## Testing
A simple test script is available at `get_request_test.py` that:
1. Starts the API server in a background thread
2. Waits for server initialization
3. Makes a test request to the `/gacha-simulate` endpoint
4. Prints the results as a pandas DataFrame

Run with:
```bash
python get_request_test.py
```

## Data Source

All the students data is sourced from the Blue Archive Wiki community database:

https://bluearchive.wiki/wiki/Characters

Data is transformed into a structured API format with filtering, pagination, and developer-friendly access.

This project is an unofficial fan-made API and is not affiliated with Nexon, NAT Games, or the Blue Archive Wiki team.

If any maintainers or rights holders would like content modified or removed, please open an issue or contact the project maintainer.