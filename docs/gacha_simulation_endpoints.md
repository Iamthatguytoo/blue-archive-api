# Simulate Gacha

As of now there will be two types of this endpoint, the old system(spark) and new system(pity), Use both of these when you want realistic pull statistics across many trials.

---

## Gacha Terms

| Term | Meaning |
|------|---------|
| **Pyroxene** | Blue Archive's premium currency. **120 Pyroxene = 1 pull** |
| **Featured Rate** | The probability that a pull results in the featured student (typically 0.7%) |
| **3★ Pity** | Guarantees a 3★ after a configurable number of pulls without obtaining one |
| **Banner Pity** | In `/v2/gacha-simulate/pity`, after 100 banner pulls without obtaining the featured student, the next guaranteed 3★ has a 50% chance of being the featured student |
| **Spark** | In `/v2/gacha-simulate/spark`, guarantees the featured student after reaching the configured spark threshold (typically 200 pulls) |

---

## Probability Format

All probability values use decimal format:

```
0.007 = 0.7%
0.03  = 3%
0.8   = 80%
```

### Spark
```bash
curl -X POST "https://blue-archive-api--JohnArchive.replit.app/v2/gacha-simulate/spark" \
-H "Content-Type: application/json" \
-H "x-api-key: YOUR_API_KEY" \
-d '{
  "simulations": 100,
  "pyroxene": 24000,
  "featured_rate": 0.007,
  "continue_after_featured": true,
  "three_star_rate": 0.03,
  "pity_threshold": 100,
  "spark_threshold": 200
}'
```

Windows (PowerShell):
```powershell
Invoke-WebRequest `
-Method POST `
-Uri "https://blue-archive-api--JohnArchive.replit.app/v2/gacha-simulate/spark" `
-Headers @{
  "Content-Type" = "application/json"
  "x-api-key" = "YOUR_API_KEY"
} `
-Body '{
  "simulations": 100,
  "pyroxene": 24000,
  "featured_rate": 0.007,
  "continue_after_featured": true,
  "three_star_rate": 0.03,
  "pity_threshold": 100,
  "spark_threshold": 200
}'
```

Python:
```python
import requests
res = requests.post(
    "https://blue-archive-api--JohnArchive.replit.app/v2/gacha-simulate/spark",
    headers={"x-api-key": "YOUR_API_KEY"},
    json={
        "simulations": 100,
        "pyroxene": 24000,
        "featured_rate": 0.007,
        "continue_after_featured": True,
        "three_star_rate": 0.03,
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
  "average_pulls_to_success": 104.71,
  "median_pulls_to_success": 102,
  "successful_runs": 100,
  "zero_success": 0,
  "trials_reached_spark": 100,
  "spark_rate": 1,
  "max_pulls": 200,
  "min_pulls": 2,
  "natural_featured_trials_count": 77,
  "sparked_featured_trials_count": 23,
  "total_featured_obtained": 100,
  "average_off_banner_3stars": 4.49,
  "all_one_stars": 15723,
  "all_two_stars": 3667,
  "all_three_stars": 610,
  "average_one_stars": 157.23,
  "average_two_stars": 36.67,
  "average_three_stars": 6.1,
  "example_pull_log": [
    "1★",
    "3★",
    "1★",
    "1★",
    "1★",
    "1★",
    "1★",
    "1★",
    "2★",
    "1★"
  ]
}
```

</details>

### Pity
```bash
curl -X POST "https://blue-archive-api--JohnArchive.replit.app/v2/gacha-simulate/pity" \
-H "Content-Type: application/json" \
-H "x-api-key: YOUR_API_KEY" \
-d '{
  "simulations": 100,
  "pyroxene": 24000,
  "featured_rate": 0.007,
  "continue_after_featured": true,
  "three_star_rate": 0.03,
  "pity_threshold": 100
}'
```

Windows (PowerShell):
```powershell
Invoke-WebRequest `
-Method POST `
-Uri "https://blue-archive-api--JohnArchive.replit.app/v2/gacha-simulate/pity" `
-Headers @{
  "Content-Type" = "application/json"
  "x-api-key" = "YOUR_API_KEY"
} `
-Body '{
  "simulations": 100,
  "pyroxene": 24000,
  "featured_rate": 0.007,
  "continue_after_featured": true,
  "three_star_rate": 0.03,
  "pity_threshold": 100
}'
```

Python:
```python
import requests
res = requests.post(
    "https://blue-archive-api--JohnArchive.replit.app/v2/gacha-simulate/pity",
    headers={"x-api-key": "YOUR_API_KEY"},
    json={
        "simulations": 100,
        "pyroxene": 24000,
        "featured_rate": 0.007,
        "continue_after_featured": True,
        "three_star_rate": 0.03,
        "pity_threshold": 100
    }
)
print(res.json())
```

<details>
<summary>Example output</summary>

```json
{
  "simulations_conducted": 100,
  "pulls_per_trial": 240,
  "success_rate": 1,
  "average_pulls_to_success": 91.94,
  "median_pulls_to_success": 100,
  "successful_runs": 100,
  "zero_success": 0,
  "max_pulls": 200,
  "min_pulls": 1,
  "natural_featured_trials_count": 89,
  "average_off_banner_3stars": 5.78,
  "all_one_stars": 18843,
  "all_two_stars": 4339,
  "all_three_stars": 818,
  "average_one_stars": 188.43,
  "average_two_stars": 43.39,
  "average_three_stars": 8.18,
  "example_pull_log": [
    "1★",
    "1★",
    "1★",
    "1★",
    "1★",
    "2★",
    "1★",
    "1★",
    "1★",
    "1★"
  ]
}
```

</details>

---

## Field References
  - Input: 

  | Field | Type | Description |
  |-----------|------|-------------|
  | `simulations` | int | Number of trial runs (1–1,000) |
  | `pyroxene` | int | Amount of Pyroxene per trial (120 = 1 pull) |
  | `featured_rate` | float | Rate-up student probability (e.g. 0.007) |
  | `continue_after_featured` | bool | Conditional about continuing to pull after featured |
  | `three_star_rate` | float | Overall 3★ rate (e.g. 0.03 for 3%) |
  | `pity_threshold` | int | Pulls before a guaranteed 3★ (typically 100) |
  | `spark_threshold` | int | (`/v2/gacha-simulate/spark`)Pulls before a guaranteed rate-up (typically 200) |
  
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
  | `trials_reached_spark` | int | (Spark system only) Trials that required the guaranteed rate-up spark |
  | `spark_rate` | float | (Spark system only) Percentage of trials that needed to spark |
  | `max_pulls` | int | Most amount of pulls used in a single trial |
  | `min_pulls` | int | Least amount of pulls used in a single trial |
  | `natural_featured_trials_count` | int | Number of trials where the featured student was obtained before the final guarantee |
  | `average_off_banner_3stars` | float | Average number of non-rate-up 3★ students obtained per simulation |
  | `all_one/two/three_stars` | int | Total number of 1★, 2★, and 3★ students obtained across all simulations |
  | `average_one/two/three_stars` | float | Average number of 1★, 2★, and 3★ students obtained per simulation |
  | `example_pull_log` | list[str] | Example results from the first 10-pull batch of the first simulation trial |

---