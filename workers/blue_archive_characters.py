import pandas as pd
import asyncio
from playwright.async_api import async_playwright
from db.database_async import student_collection, scraper_collection
from datetime import datetime, timezone, timedelta

pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)


async def should_scrape():
    job = await scraper_collection.find_one({"_id": "students_scraper"})

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


async def update_scraper_status(status):
    data = {"status": status}

    if status == "success":
        data["last_run"] = datetime.now(timezone.utc)

    await scraper_collection.update_one(
        {"_id": "students_scraper"}, {"$set": data}, upsert=True
    )


async def get_characters():

    if not await should_scrape():
        return

    async with async_playwright() as p:

        await student_collection.create_index(
            "wiki_url",
            unique=True,
        )

        browser = await p.chromium.launch()

        try:
            context = await browser.new_context(
                user_agent="BlueArchiveAPIBot/1.0 (Miraheze; Contact: User:Iamthatguytoo)"
            )
            page = await context.new_page()

            await page.goto(
                "https://bluearchive.wiki/wiki/Characters",
                wait_until="networkidle",
                timeout=120000,
            )

            all_students = page.locator("table#charactertable")
            await all_students.wait_for(state="visible", timeout=60000)

            all_rows = all_students.locator("tr[data-school]")

            rows = await all_rows.count()
            print(rows)

            student_list = []

            for i in range(rows):
                row = all_rows.nth(i)

                name_link = row.locator("td:nth-child(2) a").first

                student_name = await name_link.inner_text()
                wiki_url = await name_link.get_attribute("href")

                damage_type = await row.get_attribute("data-attack")
                armor_type = await row.get_attribute("data-armor")
                school = await row.get_attribute("data-school")
                weapon = await row.get_attribute("data-weapon")
                class_name = await row.get_attribute("data-class")
                position = await row.get_attribute("data-position")
                pool = await row.get_attribute("data-pool")
                variant = await row.get_attribute("data-variant")

                urban_terrain = await row.get_attribute("data-urban")
                outdoor_terrain = await row.get_attribute("data-outdoors")
                indoor_terrain = await row.get_attribute("data-indoors")

                rarity = await row.get_attribute("data-rarity")

                base_name = student_name.split(" (")[0]

                student_list.append({
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
                    "wiki_url": wiki_url
                })

            for student in student_list:
                await student_collection.update_one(
                    {"wiki_url": student["wiki_url"]},
                    {"$set": student},
                    upsert=True,
                )

            print(f"Processed {len(student_list)} students")


            df = pd.DataFrame(student_list)
            print(df)

            await update_scraper_status("success")

        except Exception as e:
            print(f"Scraper failed: {e}")
            await update_scraper_status("failed")

            raise

        finally:
            await browser.close()


if __name__ == "__main__":
    asyncio.run(get_characters())
