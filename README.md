# Fan Made Blue Archive API

A Fan-Made FastAPI-based API for querying Blue Archive students (characters) data, gacha calculations, pull simulations, and probability analysis.

> **Disclaimer:** This is an unofficial fan project. Not affiliated with Nexon, NAT Games, or the Blue Archive Wiki team.

## API Status


API link: [https://blue-archive-api--JohnArchive.replit.app](https://blue-archive-api--JohnArchive.replit.app)

Docs link: [Swagger UI](https://blue-archive-api--JohnArchive.replit.app/docs)

ReDoc link: [ReDoc](https://blue-archive-api--JohnArchive.replit.app/redoc)

Server status: online 🟢


---

## Why use this API?

- **Are you planning pulls for a new banner?** Use `/v2/gacha-calculate` to instantly see if your current Pyroxenes are enough to get the rate-up naturally, or whether you'll need to spark.
- **Are you not sure if you'll need to spark?** `/v2/gacha-simulate/spark` can run up to 1,000 Monte Carlo trial pulls so you can see realistic odds, average pulls to success, and how often sparking is actually needed.
- **Want to see the effect of the game's pity system?** `/v2/gacha-simulate/pity` can run up to 1,000 Monte Carlo trial pulls to estimate how often you'll naturally obtain the rate-up student, how many pulls it takes on average, and how the new system differs from the old one.
- **Do you want to know your confidence level?** `/v2/analyze-pulls` works in reverse. You give it a target probability (e.g. 80% chance) and it tells you exactly how many pulls and Pyroxenes you need.
- **Are you looking for specific students?** `/v2/students` lets you filter by school, weapon, terrain rating, damage type, and more — great for team building tools or wikis.

---

## Quick Start

**1. Register for a free API key:**
```bash
curl -X POST https://blue-archive-api--JohnArchive.replit.app/v2/auth/register
```

**2. Save your key** — it's only shown once.

**3. Make your first request:**
```bash
curl -H "x-api-key: YOUR_KEY" \
"https://blue-archive-api--JohnArchive.replit.app/v2/students?name=Hina"
```

## Features

- Retrieve student data from MongoDB with filtering and pagination (server-side cached for fast repeated queries).
- Generate and verify API keys for secure access (1,000 requests/day).
- Calculate gacha pull probabilities and spark reachability.
- Simulate gacha pulls with Monte Carlo statistical analysis (up to 1,000 simulations).
- Analyze a pull target by desired confidence level.

---

## Rate Limits

Each endpoint has a per-IP rate limit:

```
/v2/auth/register                        → 2/hour
/v2/students                             → 60/minute
/v2/banners                              → 60/minute
/v2/gacha-calculate                      → 15/minute
/v2/gacha-simulate/spark                 → 15/minute
/v2/gacha-simulate/pity                  → 15/minute
/v2/analyze-pulls                        → 30/minute
```

---

## Project Structure
```
blue_archive_api/
├── .github/
│   └── workflows/
│       ├── pytests.yml
│       └── scrape.yml
├── api/
│   ├── v1/
│   │   ├── __init__.py
│   │   └── endpoints.py
│   └── v2/
│       ├── __init__.py
│       └── endpoints.py
├── auth/
│   ├── v1/
│   │   ├── __init__.py
│   │   ├── create_random_key.py
│   │   └── key_verification.py
│   └── v2/
│       ├── __init__.py
│       ├── create_random_key.py
│       └── key_verification.py
├── db/
│   ├── __init__.py
│   ├── database.py
│   ├── database_async.py
│   └── settings.py
├── middleware/
│   └── v1/
│       ├── __init__.py
│       └── rate_limit.py
├── schemas/
│   ├── v1/
│   │   ├── __init__.py
│   │   └── schema.py
│   └── v2/
│       ├── __init__.py
│       └── schema.py
├── services/
│   ├── v1/
│   │   ├── __init__.py
│   │   ├── analyze_pulls.py
│   │   ├── cache_requests.py
│   │   ├── gacha_calculate.py
│   │   ├── gacha_simulate.py
│   │   ├── health_check.py
│   │   └── retrieve_students.py
│   └── v2/
│       ├── __init__.py
│       ├── gacha_simulate_pity.py
|       ├── gacha_simulate_spark.py
│       ├── health_check.py
│       ├── retrieve_banners.py
│       └── retrieve_students.py
├── docs/
│   ├── analyze_pulls_endpoint.md
│   ├── banner_endpoint.md
│   ├── gacha_calculate_endpoint.md
│   ├── gacha_simulation_endpoints.md
│   ├── general_endpoints.md
│   └── students_endpoint.md
│ 
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_analyze.py
│   ├── test_calculate.py
│   ├── test_simulate.py
│   ├── v1/
│   │   ├── __init__.py
│   │   ├── test_auth.py
│   │   ├── test_health.py
│   │   └── test_student.py
│   └── v2/
│       ├── __init__.py
│       ├── test_auth.py
│       ├── test_banner.py
│       ├── test_health.py
│       └── test_student.py
├── utils/
│   ├── gacha_pulls.py
│   └── serializers.py
├── workers/
|   ├── banner_scraper.py
|   └── blue_archive_characters.py
├── blue_archive_characters_api.py
├── docs_and_examples.py
├── requirements.txt
├── .gitignore
├── .replit
└── README.md
```

---
## Tech Stack
- **Python**: Main Programming Language
- **FastAPI**: Framework for the API
- **MongoDB**: Main database
- **Pytest**: For testing the functions and response codes
- **GitHub Actions**: CI and scheduled workflows
- **Replit**: Main deployment platform
---

## API Endpoints Information

- [General Endpoints](docs/general_endpoints.md)
- [Student Endpoint](docs/students_endpoint.md)
- [Gacha Calculation Endpoint](docs/gacha_calculate_endpoint.md)
- [Gacha Simulation Endpoints](docs/gacha_simulation_endpoints.md)
- [Analyze Pulls Endpoints](docs/analyze_pulls_endpoint.md)
- [Banner Endpoint](docs/banner_endpoint.md)

## Notes

- Your API key is shown only once at registration. Store and keep the key somewhere safe
- All endpoints except `/`, `/health`, and `/v2/auth/register` require the `x-api-key` header
- All keys have a 1,000 request/day limit, reset daily
- Student data responses are cached server-side for fast repeated queries

---

## Data Source

All student data is sourced from the Blue Archive Wiki community database:

- https://bluearchive.wiki/wiki/Characters

Data is transformed into a structured API format with filtering, pagination, and developer-friendly access.

This project is an unofficial fan-made API and is not affiliated with Nexon, NAT Games, or the Blue Archive Wiki team.

If any maintainers or rights holders would like content modified or removed, please open an issue or contact the project maintainer.
