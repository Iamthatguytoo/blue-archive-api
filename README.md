# Fan Made Blue Archive API

A Fan-Made FastAPI-based API for querying Blue Archive students (characters) data, gacha calculations, pull simulations, and probability analysis.

## Disclaimer

This repository is intended for demonstration purposes only.
It is not a complete or production-ready package, and may be missing configuration or dependencies required for deployment.


## API Status
```
-API link: https://blue-archive-api--JohnArchive.replit.app
-Server status: offline 🔴
```
## Main API Requests

#### Probability format
All probability values use decimal format
```Examples
- 0.007 = 0.7%
- 0.03 = 3%
- 0.8 = 80%
```

### Register an API key:

```bash
curl -X POST https://blue-archive-api--JohnArchive.replit.app/auth/register
```

-or in Windows:

```powershell
Invoke-RestMethod -Method POST -Uri "https://blue-archive-api--JohnArchive.replit.app/auth/register"
```

### Query students:

```bash
curl -H "x-api-key: YOUR_KEY" \
"https://blue-archive-api--JohnArchive.replit.app/students?name=Hina"
```
-or in Windows:

```powershell
Invoke-WebRequest `
  -Uri "https://blue-archive-api--JohnArchive.replit.app/students?name=Hina" `
  -Headers @{ "x-api-key" = "YOUR_API_KEY" }
```

### Calculate Pulls:

```bash
curl -X POST "https://blue-archive-api--JohnArchive.replit.app/gacha-calculate" \
-H "Content-Type: application/json" \
-H "x-api-key: YOUR_API_KEY" \
-d '{
  "pyroxene": 24000,
  "rate_up": 0.007
}'
```

-or in Windows:

```powershell
Invoke-WebRequest `
-Method POST `
-Uri "https://blue-archive-api--JohnArchive.replit.app/gacha-calculate" `
-Headers @{
  "Content-Type" = "application/json"
  "x-api-key" = "YOUR_API_KEY"
} `
-Body '{
  "pyroxene": 24000,
  "rate_up": 0.007
}'
```

### Simulate Gacha:

```bash
curl -X POST "https://blue-archive-api--JohnArchive.replit.app/gacha-simulate" \
-H "Content-Type: application/json" \
-H "x-api-key: YOUR_API_KEY" \
-d '{
  "simulations": 100,
  "pyroxene": 24000,
  "rate_up": 0.007,
  "rate_up_3_star": 0.03,
  "pity_threshold": 100,
  "spark_threshold": 200
}'
```

-or in Windows:

```powershell
Invoke-WebRequest `
-Method POST `
-Uri "https://blue-archive-api--JohnArchive.replit.app/gacha-simulate" `
-Headers @{
  "Content-Type" = "application/json"
  "x-api-key" = "YOUR_API_KEY"
} `
-Body '{
  "simulations": 100,
  "pyroxene": 24000,
  "rate_up": 0.007,
  "rate_up_3_star": 0.03,
  "pity_threshold": 100,
  "spark_threshold": 200
}'
```

### Analyze Pulls:

```bash
curl -X POST "https://blue-archive-api--JohnArchive.replit.app/analyze-pulls" \
-H "Content-Type: application/json" \
-H "x-api-key: YOUR_API_KEY" \
-d '{
  "probability": 0.8,
  "rate_up": 0.007
}'
```

-or in Windows:

```powershell
Invoke-WebRequest `
-Method POST `
-Uri "https://blue-archive-api--JohnArchive.replit.app/analyze-pulls" `
-Headers @{
  "Content-Type" = "application/json"
  "x-api-key" = "YOUR_API_KEY"
} `
-Body '{
  "probability": 0.8,
  "rate_up": 0.007
}'
```

## Features

- Retrieve student data from MongoDB with filtering and pagination
- Generate and verify API keys for secure access
- Calculate gacha pull probabilities and spark reachability
- Simulate gacha pulls with statistical analysis
- Analyze pull targets for desired students

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
    - simulations: int (1-1000)
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

### Docs
- Interactive API docs are available at:
  - /docs
  - /redoc 

## Notes
- The API key is only shown once upon generation - store it securely
- All protected endpoints require the `x-api-key` header with a valid key

## Data Source

All the students data is sourced from the Blue Archive Wiki community database:

https://bluearchive.wiki/wiki/Characters

Data is transformed into a structured API format with filtering, pagination, and developer-friendly access.

This project is an unofficial fan-made API and is not affiliated with Nexon, NAT Games, or the Blue Archive Wiki team.

If any maintainers or rights holders would like content modified or removed, please open an issue or contact the project maintainer.
