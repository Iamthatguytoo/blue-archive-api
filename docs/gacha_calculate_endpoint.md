# Calculate Pulls

Use this when you want to know: "I have X Pyroxenes — what are my chances?"

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
curl -X POST "https://blue-archive-api--JohnArchive.replit.app/v2/gacha-calculate" \
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
-Uri "https://blue-archive-api--JohnArchive.replit.app/v2/gacha-calculate" `
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
    "https://blue-archive-api--JohnArchive.replit.app/v2/gacha-calculate",
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

## Field References
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

---