# Register an API key

```bash
curl -X POST https://blue-archive-api--JohnArchive.replit.app/v2/auth/register
```

Windows (PowerShell):
```powershell
Invoke-RestMethod -Method POST -Uri "https://blue-archive-api--JohnArchive.replit.app/v2/auth/register"
```

Python:
```python
import requests
res = requests.post("https://blue-archive-api--JohnArchive.replit.app/v2/auth/register")
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

## Field References

### General
- `GET /` — Landing page with API status and documentation links.
- `GET /health` — Health check, returns server status (useful for uptime monitoring).

### Authentication
- `POST /v2/auth/register` — Generate a new API key (returns `sk_*` key to user(shown only once) and adds the hashed version to the database).

### Interactive Docs
- `/docs` — Swagger UI (try endpoints directly in the browser)
- `/redoc` — ReDoc (clean reference documentation)

---