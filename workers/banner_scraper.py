import asyncio
import re
from datetime import datetime, timedelta
from playwright.async_api import async_playwright
from db.database_async import banner_collection
from utils.serializers import serialize_banner, normalize_banner_timezone

current_year = datetime.now().year

async def get_banners():
    async with async_playwright() as p:

        browser = await p.chromium.launch()

        try:
            context = await browser.new_context(
                user_agent="BlueArchiveAPIBot/1.0 (Miraheze; Contact: User:Iamthatguytoo)"
            )

            page = await context.new_page()

            await page.goto(
                "https://bluearchive.wiki/wiki/Main_Page",
                wait_until="domcontentloaded",
                timeout=120000,
            )

            banner_frame = page.locator("div.tabs-content.tabs-content-2").nth(0)

            banner_list = []

            paragraphs = banner_frame.locator("p")

            for i in range(await paragraphs.count()):

                paragraph = paragraphs.nth(i)

                dates = paragraph.locator("span.datetime")

                if await dates.count() < 2:
                    continue

                start_datetime = await dates.nth(0).get_attribute(
                    "data-datetime"
                )
                end_datetime = await dates.nth(1).get_attribute(
                    "data-datetime"
                )

                if not start_datetime or not end_datetime:
                    continue

                start_date = datetime.fromisoformat(
                    start_datetime.replace("Z", "+00:00")
                )

                end_date = datetime.fromisoformat(
                    end_datetime.replace("Z", "+00:00")
                )

                links = paragraph.locator("a[href^='/wiki/']")

                names = []

                for n in range(await links.count()):

                    link = links.nth(n)

                    name = await link.get_attribute("title")

                    if name and name not in names:
                        names.append(name)

                if not names:
                    continue

                for name in names:

                    banner_list.append(
                        {
                            "name": name,
                            "start_date": start_date,
                            "end_date": end_date,
                        }
                    )

            return banner_list

        except Exception as e:
            print(f"Scraper failed: {e}")
            raise

        finally:
            await browser.close()

async def main():

    banners = await get_banners()

    print(f"Scraped {len(banners)} banners")

    if not banners:
        print("No banners were scraped. Aborting database update.")
        return 
    
    curr_banners = banner_collection.find({})
    banner_check = await curr_banners.to_list(length=None)

    banner_check = [serialize_banner(banner) for banner in banner_check]

    banners = [normalize_banner_timezone(banner) for banner in banners]
    banner_check = [normalize_banner_timezone(banner) for banner in banner_check]

    if banners == banner_check:
        print("No new banners detected")
        return

    await banner_collection.delete_many({})
    await banner_collection.insert_many(banners)

    print("Banner data successfully updated")

if __name__ == "__main__":
    asyncio.run(main())