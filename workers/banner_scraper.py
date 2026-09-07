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

            all_banners = page.locator("div.tabs-content.tabs-content-2")

            banner_frame = all_banners.nth(0)

            text = await banner_frame.inner_text()

            banner_list = []

            for line in text.splitlines():

                line = line.replace("\xa0", " ").strip()

                if not line:
                    continue

                match = re.fullmatch( r"^(.*?):\s*" r"(\d{2}/\d{2})\s*[–-]\s*" r"(\d{2}/\d{2})$", line,)

                if not match:
                    print(f"Skipping: {line!r}")
                    continue

                name, start_date_str, end_date_str = match.groups()

                start_date = datetime.strptime(f"{start_date_str}/{current_year}", "%m/%d/%Y",)

                end_date = datetime.strptime(f"{end_date_str}/{current_year}", "%m/%d/%Y",)

                if end_date < start_date:
                    end_date += timedelta(days=365)

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