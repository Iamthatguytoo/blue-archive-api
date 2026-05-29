# Fan Made Blue Archive API

A Fan-Made FastAPI-based API for querying Blue Archive students (characters) data, gacha calculations, pull simulations, and probability analysis.

## Disclaimer

This repository is intended for demonstration purposes only.
It is not a complete or production-ready package, and may be missing configuration or dependencies required for deployment.

## Project Status
Experimental

## API Status
```
-API link: https://blue-archive-api--JohnArchive.replit.app
-Server status: online 🟢
```

## Features

- Retrieve student data from MongoDB with filtering and pagination
- Generate and verify API keys for secure access
- Calculate gacha pull probabilities and spark reachability
- Simulate gacha pulls with statistical analysis
- Analyze pull targets for desired students

## Main API Requests

#### Probability format
All probability values use decimal format
```Examples
- 0.007 = 0.7%
- 0.03 = 3%
- 0.8 = 80%
```

#### Rate limit
Each endpoint has a limit per minute or hour:
```
- /auth/register: 2/hour
- /students: 60/minute
- /gacha-calculate and /gacha-simulate: 15/minute
- /analyze-pulls: 30/minute
```

### Register an API key:

```bash
curl -X POST https://blue-archive-api--JohnArchive.replit.app/auth/register
```

-or in Windows:

```powershell
Invoke-RestMethod -Method POST -Uri "https://blue-archive-api--JohnArchive.replit.app/auth/register"
```

<details>
<summary>- Example output:</summary>

```json
{
  "api_key": "sk_********************************",
  "daily_limit": 1000,
  "tier": "free",
  "resetted_at": "2026-XX-XX",
  "message": "Copy this string now. You wont see it again"
}
```

</details>

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
<details>
<summary>- Example output:</summary>
  
```json
{
  "total": 3,
  "skip": 0,
  "limit": 20,
  "students": [
    {
      "name": "Hina (Dress)",
      "base_name": "Hina",
      "rarity": "3",
      "variant": "dress",
      "damage_type": "explosive",
      "armor_type": "elastic",
      "class_name": "striker",
      "school": "gehenna",
      "position": "back",
      "weapon": "mg",
      "pool": "anniversary",
      "terrain": {
        "urban_terrain": "D",
        "outdoor_terrain": "A",
        "indoor_terrain": "S"
      }
    },
    {
      "name": "Hina (Swimsuit)",
      "base_name": "Hina",
      "rarity": "3",
      "variant": "swimsuit",
      "damage_type": "explosive",
      "armor_type": "heavy",
      "class_name": "striker",
      "school": "gehenna",
      "position": "back",
      "weapon": "mg",
      "pool": "limited",
      "terrain": {
        "urban_terrain": "B",
        "outdoor_terrain": "S",
        "indoor_terrain": "D"
      }
    },
    {
      "name": "Hina",
      "base_name": "Hina",
      "rarity": "3",
      "variant": "none",
      "damage_type": "explosive",
      "armor_type": "heavy",
      "class_name": "striker",
      "school": "gehenna",
      "position": "back",
      "weapon": "mg",
      "pool": "archive",
      "terrain": {
        "urban_terrain": "S",
        "outdoor_terrain": "C",
        "indoor_terrain": "C"
      }
    }
  ]
}
```

</details>

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

<details>
<summary>- Example output:</summary>

```json
{
  "pulls": 200,
  "spark_reachable": true,
  "pulls_to_spark": 0,
  "chance_get_rate_up_naturally": 75.461405,
  "chance_need_spark": 24.538595
}
```

</details>

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

<details>
<summary>- Example output:</summary>

```json
{
  "simulations_conducted": 100,
  "pulls_per_trial": 200,
  "success_rate": 1,
  "average_pulls_to_success": 119.09,
  "median_pulls_to_success": 124.5,
  "succesful_runs": 100,
  "zero_success": 0,
  "trials_reached_spark": 26,
  "max_pulls": 200,
  "min_pulls": 2,
  "rate_up_obtained": 74,
  "average_off_banner_3stars": 2.77
}
```

</details>

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

<details>
<summary>- Example output:</summary>

```json
{
  "required_pulls": 230,
  "pyroxene_needed": 27600,
  "confidence": 0.8,
  "risk_level": "moderate"
}
```

</details>

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
