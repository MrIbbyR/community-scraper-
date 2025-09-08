import asyncio
import csv
from playwright.async_api import async_playwright

COMMUNITY_URL = "https://www.smartrecruiters.com/app/communities/details/43958b7e-97b4-4465-9ed2-5324193e8c8f/prospects"
OUTPUT_CSV = "prospect_emails.csv"

# Updated selector for email inside candidate personal info block
EMAIL_TEXT_SELECTOR = "sr-candidate-personal-info spl-typography-body"

async def extract_email(profile_tab):
    elements = await profile_tab.query_selector_all(EMAIL_TEXT_SELECTOR)
    for el in elements:
        text = (await el.inner_text()).strip()
        if "@" in text and "." in text:
            return text
    return ""

async def run():
    async with async_playwright() as p:
        print("🚀 Connecting to real Chrome (CDP)...")
        browser = await p.chromium.connect_over_cdp("http://localhost:9222")
        context = browser.contexts[0]
        page = await context.new_page()

        print("🌐 Navigating to Community Prospects page...")
        await page.goto(COMMUNITY_URL)
        await page.wait_for_selector('a[href^="/app/people/applications/"]', timeout=15000)

        print("🔄 Scrolling to load all prospects...")
        seen = set()
        same_count = 0

        while same_count < 5:
            links = await page.query_selector_all('a[href^="/app/people/applications/"]')
            new_links = 0

            for link in links:
                href = await link.get_attribute('href')
                if href and href not in seen:
                    seen.add(href)
                    new_links += 1

            if new_links == 0:
                same_count += 1
            else:
                same_count = 0

            await page.mouse.wheel(0, 2000)
            await page.wait_for_timeout(1500)

        print(f"✅ Total unique profiles found: {len(seen)}")
        emails = []

        for idx, href in enumerate(seen):
            full_url = "https://www.smartrecruiters.com" + href
            print(f"➡️ Opening profile #{idx + 1}: {full_url}")
            profile_tab = await context.new_page()

            try:
                await profile_tab.goto(full_url)
                await profile_tab.wait_for_load_state("networkidle")
                await profile_tab.wait_for_selector(EMAIL_TEXT_SELECTOR, timeout=10000)

                email = await extract_email(profile_tab)
                if email:
                    print(f"📧 Found: {email}")
                    emails.append([email])
                else:
                    print("❌ Empty or missing email.")
            except Exception as e:
                print(f"⚠️ Failed to scrape profile #{idx + 1}: {e}")
            finally:
                await profile_tab.close()
                await asyncio.sleep(0.5)

        print("💾 Saving to CSV...")
        with open(OUTPUT_CSV, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Email"])
            writer.writerows(emails)

        print(f"✅ Done. {len(emails)} emails saved to {OUTPUT_CSV}")

if __name__ == "__main__":
    asyncio.run(run())
