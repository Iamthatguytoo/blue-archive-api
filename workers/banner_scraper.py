import asyncio
import re
from playwright.async_api import async_playwright
from db.database_async import banner_collection
from utils.serializers import serialize_banner, normalize_banner_timezone
from datetime import datetime
from utils.github_outputs import set_github_output

current_year = datetime.now().year

async def get_banners():

    async with async_playwright() as p:

        browser = await p.chromium.launch()

        try:
            page = await browser.new_page()

            await page.set_extra_http_headers({
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/117.0.0.0 Safari/537.36"
                )
            })

            await page.goto(
                "https://bluearchive.wiki/wiki/Main_Page",
                wait_until="domcontentloaded",
                timeout=120000,
            )

            all_banners = page.locator("div.tabs-content.tabs-content-2")

            banner_frame = all_banners.nth(0)

            print("Current URL:", page.url)
            print("Page title:", await page.title())

            print(
                "Banner locator count:",
                await page.locator("div.tabs-content.tabs-content-2").count()
            )

            body_text = await page.locator("body").inner_text()
            print("BODY START:")
            print(body_text[:2000])


            text = await banner_frame.inner_text()

            banner_list = []

            for line in text.splitlines():

                line = line.strip()

                if not line:
                    continue

                match = re.fullmatch(
                    r"^(.*?):\s*(\d{2}/\d{2})\s*-\s*(\d{2}/\d{2})$",
                    line
                )

                if not match:
                    print(f"Skipping: {line!r}")
                    continue

                name, start_date, end_date = match.groups()

                start_date = datetime.strptime(f"{start_date}/{current_year}", "%m/%d/%Y")
                end_date = datetime.strptime(f"{end_date}/{current_year}", "%m/%d/%Y")

                banner_list.append({
                    "name": name,
                    "start_date": start_date,
                    "end_date": end_date,
                })

            return banner_list

        except Exception as e:
            print(f"Scraper failed: {e}")
            raise

        finally:
            await browser.close()

async def main():
    banners = await get_banners()
    curr_banners = banner_collection.find({})
    banner_check = await curr_banners.to_list(length=None) 

    banner_check = [serialize_banner(banner) for banner in banner_check]

    banners = [normalize_banner_timezone(banner) for banner in banners]
    banner_check = [normalize_banner_timezone(banner) for banner in banner_check]

    if banners == banner_check:
        print("No new banners detected")
        set_github_output(name="updated", value="false")
        return

    await banner_collection.delete_many({})
    await banner_collection.insert_many(banners)

    print("Banner data successfully updated")
    set_github_output(name="updated", value="true")

if __name__ == "__main__":
    asyncio.run(main())