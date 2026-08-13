# Analyze Pulls

Use this when you want to know: "How many Pyroxenes do I need for an 80% chance?"

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

```bash
curl -X POST "https://blue-archive-api--JohnArchive.replit.app/v2/analyze-pulls" \
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
-Uri "https://blue-archive-api--JohnArchive.replit.app/v2/analyze-pulls" `
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
    "https://blue-archive-api--JohnArchive.replit.app/v2/analyze-pulls",
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

## Field References
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

---