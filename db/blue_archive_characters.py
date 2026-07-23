import pandas as pd
from playwright.sync_api import sync_playwright
from db.database import student_collection, scraper_collection
from datetime import datetime, timezone, timedelta

pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)

def should_scrape():
    job = scraper_collection.find_one(
        {"_id": "students_scraper"}
    )

    if not job:
        return True

    last_run = job.get("last_run")

    if not last_run:
        return True

    if last_run.tzinfo is None:
        last_run = last_run.replace(tzinfo=timezone.utc)

    if datetime.now(timezone.utc) - last_run < timedelta(weeks=2):
        print("Scrape skipped: less than 2 weeks since last run.")
        return False

    return True

def update_scraper_status(status):
    data = {
        "status": status
    }

    if status == "success":
        data["last_run"] = datetime.now(timezone.utc)

    scraper_collection.update_one(
        {"_id": "students_scraper"},
        {"$set": data},
        upsert=True
    )

def get_characters():

    if not should_scrape():
            return

    with sync_playwright() as p:
        student_collection.create_index([("base_name", 1), ("variant", 1)], unique=True)

        browser = p.chromium.launch()
        try:
            page = browser.new_page()
            page.set_extra_http_headers(
                {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
                }
            )
            page.goto(
                "https://bluearchive.wiki/wiki/Characters",
                wait_until="networkidle",
                timeout=120000,
            )

            all_students = page.locator("table#charactertable")
            all_students.wait_for(state="visible", timeout=60000)
            all_rows = all_students.locator("tr")

            rows = all_rows.count()
            print(rows)

            student_list = []
            for i in range(rows):
                row = all_rows.nth(i)

                names = row.locator("td:nth-child(2) a").all_inner_texts()
                student_name = names[0] if names else "Unknown"

                damage_type = row.get_attribute("data-attack")

                armor_type = row.get_attribute("data-armor")

                school = row.get_attribute("data-school")

                weapon = row.get_attribute("data-weapon")

                class_name = row.get_attribute("data-class")

                position = row.get_attribute("data-position")

                pool = row.get_attribute("data-pool")

                variant = row.get_attribute("data-variant")

                urban_terrain = row.get_attribute("data-urban")

                outdoor_terrain = row.get_attribute("data-outdoors")

                indoor_terrain = row.get_attribute("data-indoors")

                rarity = row.get_attribute("data-rarity")

                base_name = student_name.split(" (")[0]

                student_list.append(
                    {
                        "name": student_name,
                        "base_name": base_name,
                        "rarity": rarity,
                        "variant": variant,
                        "class": class_name,
                        "school": school,
                        "damage_type": damage_type,
                        "armor_type": armor_type,
                        "position": position,
                        "weapon": weapon,
                        "pool": pool,
                        "terrain": {
                            "urban_terrain": urban_terrain,
                            "outdoor_terrain": outdoor_terrain,
                            "indoor_terrain": indoor_terrain,
                        },
                    }
                )

            try:
                result = student_collection.insert_many(student_list, ordered=False)
                print(f"Added {len(result.inserted_ids)} students to your db")
            except Exception:
                print("Inserted some students, some duplicates were skipped.")

            df = pd.DataFrame(student_list)
            print(df)

            update_scraper_status("success")
        except Exception as e:
            print(f"Scraper failed: {e}")
            update_scraper_status("failed")
            raise

        finally:
            browser.close()

if __name__ == "__main__":
    get_characters()
