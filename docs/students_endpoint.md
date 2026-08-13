# Query students

```bash
curl -H "x-api-key: YOUR_KEY" \
"https://blue-archive-api--JohnArchive.replit.app/v2/students?name=Hina"
```

Windows (PowerShell):
```powershell
Invoke-WebRequest `
  -Uri "https://blue-archive-api--JohnArchive.replit.app/v2/students?name=Hina" `
  -Headers @{ "x-api-key" = "YOUR_API_KEY" }
```

Python:
```python
import requests
res = requests.get(
    "https://blue-archive-api--JohnArchive.replit.app/v2/students",
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

### Filtering students
You can also filter the results or combine any query parameters in a single request.
This example fetches back-row Mystic students from Millennium, skips the first two results, and returns one student.:

```bash
curl -H "x-api-key: YOUR_API_KEY" \
"https://blue-archive-api--JohnArchive.replit.app/v2/students?school=millennium&damage_type=mystic&position=back&skip=2&limit=1"
```
Windows (PowerShell):
```powershell
Invoke-WebRequest `
  -Uri "https://blue-archive-api--JohnArchive.replit.app/v2/students?school=millennium&damage_type=mystic&position=back&skip=2&limit=1" `
  -Headers @{ "x-api-key" = "YOUR_API_KEY" }
```
Python:
```python
import requests
res = requests.get(
    "https://blue-archive-api--JohnArchive.replit.app/v2/students",
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

## Field References
  - Input:

  | Parameter | Type | Description |
  |-----------|------|-------------|
  | `name` | string | Exact match, case-insensitive (e.g. `Arisu (Armed)`) |
  | `base_name` | string | Exact match with partial fallback (e.g. `Arisu` returns all Arisu variants) |
  | `school` | string | Filter by school (e.g. `gehenna`, `trinity`, `millennium`). |
  | `position` | string | Filter by position (`front`, `middle`, `back`) |
  | `damage_type` | string | Filter by damage type (`explosive`, `penetration`, `mystic`, `sonic`) |
  | `limit` | int | Results per page (default: 20) |
  | `skip` | int | Number of results to skip for pagination (default: 0) |

  - Output:

  | Parameter | Type | Description |
  |-----------|------|-------------|
  | `total` | int | Number of students fitting the input |
  | `limit` | int | Results per page (default: 20) |
  | `skip` | int | Results to skip for pagination (default: 0) |
  | `name` | string | Exact match, case-insensitive (e.g. `Arisu (Armed)`) |
  | `base_name` | string | Exact match with partial fallback (e.g. `Arisu` returns all Arisu variants) |
  | `rarity` | string | The rarity of the student(`3`, `2`, `1`) |
  | `variant` | string | Student's variant (eg. `swimsuit`, `maid`, `sportswear`) | 
  | `school` | string | Student's school (e.g. `gehenna`, `trinity`, `millennium`). |
  | `class` | string | Student's role in battle (`striker`, `special`) |
  | `damage_type` | string | Student's damage type (eg. `explosive`, `penetration`, `mystic`, `sonic`) |
  | `armor_type` | string | Student's armor type (`light`, `heavy`, `special`, `elastic`) |
  | `position` | string | The students position in gameplay (`front`, `back`, `middle`) |
  | `weapon` | string | Student's weapon type (e.g. `sr`, `smg`, `mg`, `ar`) |
  | `pool` | string | Student's banner pool (e.g. `archive`, `anniversary`) |
  | `urban_terrain` | str | How good a student is in urban terrain levels (eg. `S`, `D`, `A`) | 
  | `outdoor_terrain` | str | How good a student is in outdoor terrain levels (eg. `S`, `D`, `A`) | 
  | `indoor_terrain` | str | How good a student is in indoor terrain levels (eg. `S`, `D`, `A`) | 

---