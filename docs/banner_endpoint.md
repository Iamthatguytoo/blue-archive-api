# Get Current Banners

```bash
curl -H "x-api-key: YOUR_API_KEY" \
"https://blue-archive-api--JohnArchive.replit.app/v2/banners"
```

Windows (PowerShell):
```powershell
Invoke-WebRequest `
  -Uri "https://blue-archive-api--JohnArchive.replit.app/v2/banners" `
  -Headers @{ "x-api-key" = "YOUR_API_KEY" }
```

Python:
```python
import requests
res = requests.get(
    "https://blue-archive-api--JohnArchive.replit.app/v2/banners",
    headers={"x-api-key": "YOUR_API_KEY"}
)
print(res.json())
```

<details>
<summary>Example output</summary>

```json
{
  "banners": [
    {
      "name": "Akane (School Uniform)",
      "start_date": "2026-08-04T00:00:00Z",
      "end_date": "2026-08-18T00:00:00Z"
    },
    {
      "name": "Seia",
      "start_date": "2026-08-04T00:00:00Z",
      "end_date": "2026-08-18T00:00:00Z"
    },
    {
      "name": "Asuna (School Uniform)",
      "start_date": "2026-08-04T00:00:00Z",
      "end_date": "2026-08-18T00:00:00Z"
    },
    {
      "name": "Toki (Bunny Girl)",
      "start_date": "2026-08-04T00:00:00Z",
      "end_date": "2026-08-18T00:00:00Z"
    }
  ]
}
```

</details>

## Field References
  - Output:

  | Parameter | Type | Description |
  |-----------|------|-------------|
  | `banners` | list[SingleBannerResponse] | List of all current banners |
  | `name` | str | Student featured in the banner |
  | `start_date` | datetime | Day and time the banner starts |
  | `end_date` | datetime | Day and time the banner ends |