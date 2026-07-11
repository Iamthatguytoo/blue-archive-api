# Fan Made Blue Archive API

A Fan-Made FastAPI-based API for querying Blue Archive students (characters) data, gacha calculations, pull simulations, and probability analysis.

> **Disclaimer:** This is an unofficial fan project. Not affiliated with Nexon, NAT Games, or the Blue Archive Wiki team.

## API Status

```
API link: https://blue-archive-api--JohnArchive.replit.app
Server status: online 🟢
Interactive docs: /docs  or  /redoc
```

---

## Why use this API?

- **Are you planning pulls for a new banner?** Use `/v1/gacha-calculate` to instantly see if your current Pyroxenes are enough to get the rate-up naturally, or whether you'll need to spark.
- **Are you not sure if you'll need to spark?** `/v1/gacha-simulate` can run up to 1,000 Monte Carlo trial pulls so you can see realistic odds, average pulls to success, and how often sparking is actually needed.
- **Do you want to know your confidence level?** `/v1/analyze-pulls` works in reverse. You give it a target probability (e.g. 80% chance) and it tells you exactly how many pulls and Pyroxenes you need.
- **Are you looking for specific students?** `/v1/students` lets you filter by school, weapon, terrain rating, damage type, and more — great for team building tools or wikis.

---

## Quick Start

**1. Register for a free API key:**
```bash
curl -X POST https://blue-archive-api--JohnArchive.replit.app/v1/auth/register
```

**2. Save your key** — it's only shown once.

**3. Make your first request:**
```bash
curl -H "x-api-key: YOUR_KEY" \
"https://blue-archive-api--JohnArchive.replit.app/v1/students?name=Hina"
```

---

## Gacha Terms

| Term | Meaning |
|------|---------|
| **Pyroxene** | Blue Archive's premium currency. **120 Pyroxene = 1 pull** |
| **Rate-up** | The boosted chance for the featured student on the current banner (typically 0.7%) |
| **Pity** | A guaranteed 3★ after a set number of pulls without one (typically every 100 pulls) |
| **Spark** | A guaranteed rate-up student after reaching the spark threshold (typically 200 pulls) |

---

## Features

- Retrieve student data from MongoDB with filtering and pagination (server-side cached for fast repeated queries)
- Generate and verify API keys for secure access (1,000 requests/day)
- Calculate gacha pull probabilities and spark reachability
- Simulate gacha pulls with Monte Carlo statistical analysis (up to 1,000 simulations)
- Analyze a pull target by desired confidence level

---

## Rate Limits

Each endpoint has a per-IP rate limit:

```
/v1/auth/register                        → 2/hour
/v1/students                             → 60/minute
/v1/gacha-calculate and /v1/gacha-simulate  → 15/minute
/v1/analyze-pulls                        → 30/minute
```

---

## Probability Format

All probability values use decimal format:

```
0.007 = 0.7%
0.03  = 3%
0.8   = 80%
```

---

## API Requests

### Register an API key

```bash
curl -X POST https://blue-archive-api--JohnArchive.replit.app/v1/auth/register
```

Windows (PowerShell):
```powershell
Invoke-RestMethod -Method POST -Uri "https://blue-archive-api--JohnArchive.replit.app/v1/auth/register"
```

Python:
```python
import requests
res = requests.post("https://blue-archive-api--JohnArchive.replit.app/v1/auth/register")
print(res.json())
```

<details>
<summary>Example output</summary>

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

---

### Query students

```bash
curl -H "x-api-key: YOUR_KEY" \
"https://blue-archive-api--JohnArchive.replit.app/v1/students?name=Hina"
```

Windows (PowerShell):
```powershell
Invoke-WebRequest `
  -Uri "https://blue-archive-api--JohnArchive.replit.app/v1/students?name=Hina" `
  -Headers @{ "x-api-key" = "YOUR_API_KEY" }
```

Python:
```python
import requests
res = requests.get(
    "https://blue-archive-api--JohnArchive.replit.app/v1/students",
    headers={"x-api-key": "YOUR_API_KEY"},
    params={"name": "Hina"}
)
print(res.json())
```

<details>
<summary>Example output</summary>

```json
{
  "total": 1,
  "skip": 0,
  "limit": 20,
  "students": [
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

---

#### Filtering students
You can also filter the results or combine any query parameters in a single request.
This is an example of fetching back-row mystic-type students from Millennium skipping the first 2 and limiting/returning up to 1:

```bash
curl -H "x-api-key: YOUR_API_KEY" \
"https://blue-archive-api--JohnArchive.replit.app/v1/students?school=millennium&damage_type=mystic&position=back&skip=2&limit=1"
```
Windows (PowerShell):
```powershell
Invoke-WebRequest `
  -Uri "https://blue-archive-api--JohnArchive.replit.app/v1/students?school=millennium&damage_type=mystic&position=back&skip=2&limit=1" `
  -Headers @{ "x-api-key" = "YOUR_API_KEY" }
```
Python:
```python
import requests
res = requests.get(
    "https://blue-archive-api--JohnArchive.replit.app/v1/students",
    headers={"x-api-key": "YOUR_API_KEY"},
    params={
        "school": "millennium",
        "damage_type": "mystic",
        "position": "back",
        "skip": 2,
        "limit": 1
    }
)
print(res.json())
```

<details>
<summary>Example output</summary>

```json
{
  "total": 10,
  "skip": 2,
  "limit": 1,
  "students": [
    {
      "name": "Kei",
      "base_name": "Kei",
      "rarity": "3",
      "variant": "none",
      "damage_type": "mystic",
      "armor_type": "composite",
      "class_name": "striker",
      "school": "millennium",
      "position": "back",
      "weapon": "rg",
      "pool": "anniversary",
      "terrain": {
        "urban_terrain": "S",
        "outdoor_terrain": "D",
        "indoor_terrain": "A"
      }
    }
  ]
}
```

</details>

---

### Calculate Pulls

Use this when you want to know: "I have X Pyroxenes — what are my chances?"

```bash
curl -X POST "https://blue-archive-api--JohnArchive.replit.app/v1/gacha-calculate" \
-H "Content-Type: application/json" \
-H "x-api-key: YOUR_API_KEY" \
-d '{
  "pyroxene": 24000,
  "rate_up": 0.007
}'
```

Windows (PowerShell):
```powershell
Invoke-WebRequest `
-Method POST `
-Uri "https://blue-archive-api--JohnArchive.replit.app/v1/gacha-calculate" `
-Headers @{
  "Content-Type" = "application/json"
  "x-api-key" = "YOUR_API_KEY"
} `
-Body '{
  "pyroxene": 24000,
  "rate_up": 0.007
}'
```

Python:
```python
import requests
res = requests.post(
    "https://blue-archive-api--JohnArchive.replit.app/v1/gacha-calculate",
    headers={"x-api-key": "YOUR_API_KEY"},
    json={"pyroxene": 24000, "rate_up": 0.007}
)
print(res.json())
```

<details>
<summary>Example output</summary>

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

---

### Simulate Gacha

Use this when you want realistic pull statistics across many trials.

```bash
curl -X POST "https://blue-archive-api--JohnArchive.replit.app/v1/gacha-simulate" \
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

Windows (PowerShell):
```powershell
Invoke-WebRequest `
-Method POST `
-Uri "https://blue-archive-api--JohnArchive.replit.app/v1/gacha-simulate" `
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

Python:
```python
import requests
res = requests.post(
    "https://blue-archive-api--JohnArchive.replit.app/v1/gacha-simulate",
    headers={"x-api-key": "YOUR_API_KEY"},
    json={
        "simulations": 100,
        "pyroxene": 24000,
        "rate_up": 0.007,
        "rate_up_3_star": 0.03,
        "pity_threshold": 100,
        "spark_threshold": 200
    }
)
print(res.json())
```

<details>
<summary>Example output</summary>

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

---

### Analyze Pulls

Use this when you want to know: "How many Pyroxenes do I need for an 80% chance?"

```bash
curl -X POST "https://blue-archive-api--JohnArchive.replit.app/v1/analyze-pulls" \
-H "Content-Type: application/json" \
-H "x-api-key: YOUR_API_KEY" \
-d '{
  "probability": 0.8,
  "rate_up": 0.007
}'
```

Windows (PowerShell):
```powershell
Invoke-WebRequest `
-Method POST `
-Uri "https://blue-archive-api--JohnArchive.replit.app/v1/analyze-pulls" `
-Headers @{
  "Content-Type" = "application/json"
  "x-api-key" = "YOUR_API_KEY"
} `
-Body '{
  "probability": 0.8,
  "rate_up": 0.007
}'
```

Python:
```python
import requests
res = requests.post(
    "https://blue-archive-api--JohnArchive.replit.app/v1/analyze-pulls",
    headers={"x-api-key": "YOUR_API_KEY"},
    json={"probability": 0.8, "rate_up": 0.007}
)
print(res.json())
```

<details>
<summary>Example output</summary>

```json
{
  "required_pulls": 230,
  "pyroxene_needed": 27600,
  "confidence": 0.8,
  "risk_level": "moderate"
}
```

</details>

---

## API Endpoints Reference

### General
- `GET /` — Landing page with API status and documentation links
- `GET /health` — Health check, returns server status (useful for uptime monitoring)

### Authentication
- `POST /v1/auth/register` — Generate a new API key (returns `sk_*` key, shown only once)

### Student Data
- `GET /v1/students` — Retrieve paginated student data with filtering

  | Parameter | Type | Description |
  |-----------|------|-------------|
  | `name` | string | Exact match, case-insensitive (e.g. `Arisu (Armed)`) |
  | `base_name` | string | Exact match with partial fallback (e.g. `Arisu` returns all Arisu variants) |
  | `school` | string | Filter by school (e.g. `gehenna`, `trinity`, `millennium`) |
  | `position` | string | Filter by position (`front`, `middle`, `back`) |
  | `damage_type` | string | Filter by damage type (`explosive`, `piercing`, `mystic`, `sonic`) |
  | `armor_type` | string | Filter by armor type (`light`, `heavy`, `special`, `elastic`) |
  | `weapon` | string | Filter by weapon type (e.g. `sr`, `smg`, `mg`, `ar`) |
  | `pool` | string | Filter by banner pool (e.g. `archive`, `standard`) |
  | `limit` | int | Results per page (default: 20) |
  | `skip` | int | Results to skip for pagination (default: 0) |

### Gacha Calculations
- `POST /v1/gacha-calculate` — Calculate pull odds from Pyroxenes
  - Input:
    
  | Field | Type | Description |
  |-----------|------|-------------|
  | `pyroxene` | int | Amount of Pyroxene you have (120 = 1 pull) |
  | `rate_up` | float | Rate-up student probability (e.g. 0.007 for 0.7%) |
  
  - Output:

  | Field | Type | Description |
  |-----------|------|-------------|
  | `pulls` | int | Total pulls from your Pyroxenes |
  | `spark_reachable` | bool | Whether you have enough pulls to spark |
  | `pulls_to_spark` | int | Extra pulls still needed to reach spark (0 if already reachable) |
  | `chance_get_rate_up_naturally` | int | % chance of getting rate-up before sparking |
  | `chance_need_spark` | float | % chance you'll need to spark to guarantee the rate-up |

### Gacha Simulation
- `POST /v1/gacha-simulate` — Run Monte Carlo gacha simulations (up to 1,000 trials)
  - Input: 

  | Field | Type | Description |
  |-----------|------|-------------|
  | `simulations` | int | Number of trial runs (1–1,000) |
  | `pyroxene` | int | Amount of Pyroxene per trial (120 = 1 pull) |
  | `rate_up` | float | Rate-up student probability (e.g. 0.007) |
  | `rate_up_3_star` | float | Overall 3★ rate (e.g. 0.03 for 3%) |
  | `pity_threshold` | int | Pulls before a guaranteed 3★ (typically 100) |
  | `spark_threshold` | int | Pulls before a guaranteed rate-up (typically 200) |
  
  - Output:

  | Field | Type | Description |
  |-----------|------|-------------|
  | `simulations_conducted` | int | Number of simulations that ran |
  | `pulls_per_trial` | int | Pulls available per trial |
  | `success_rate` | float | Ratio of trials that got the rate-up student |
  | `average_pulls_to_success` | float | Average pulls needed across successful trials |
  | `median_pulls_to_success` | float | Median pulls needed across successful trials |
  | `successful_runs` | int | Trials where the rate-up was obtained |
  | `zero_success` | int | Trials where the rate-up was never obtained |
  | `trials_reached_spark` | int | Trials the required sparking |
  | `max_pulls` | int | Most amount of pulls used in a single trial |
  | `min_pulls` | int | Least amount of pulls used in a single trial |
  | `rate_up_obtained` | int | Total rate-up students obtained across all trials |
  | `average_off_banner_3stars` | float | Average non-rate-up 3 stars/★ students per trial |

### Pull Analysis
- `POST /v1/analyze-pulls` — Reverse probability: find pulls needed for a target confidence
  - Input: 

  | Field | Type | Description |
  |-----------|------|-------------|
  | `probability` | float | Your target confidence level (e.g. 0.8 for 80%) |
  | `rate_up` | float | Rate-up student probability (e.g. 0.007 for 0.7%) |
  
  - Output:
  
  | Field | Type | Description |
  |-----------|------|-------------|
  | `required_pulls` | int | Pulls needed to reach your target confidence |
  | `pyroxene_needed` | int | Pyroxenes needed (required_pulls × 120) |
  | `confidence` | float | The confidence level you requested |
  | `risk_level` | string | Assessment of the cost: low(>=0.9 or 90%), moderate(>=0.7 or 70%), or high(<70%) |

### Interactive Docs
- `/docs` — Swagger UI (try endpoints directly in the browser)
- `/redoc` — ReDoc (clean reference documentation)

---

## Notes

- Your API key is shown only once at registration. Store and keep the key somewhere safe
- All endpoints except `/`, `/health`, and `/v1/auth/register` require the `x-api-key` header
- All keys have a 1,000 request/day limit, reset daily
- Student data responses are cached server-side for fast repeated queries

---

## Data Source

All student data is sourced from the Blue Archive Wiki community database:

https://bluearchive.wiki/wiki/Characters

Data is transformed into a structured API format with filtering, pagination, and developer-friendly access.

This project is an unofficial fan-made API and is not affiliated with Nexon, NAT Games, or the Blue Archive Wiki team.

If any maintainers or rights holders would like content modified or removed, please open an issue or contact the project maintainer.
