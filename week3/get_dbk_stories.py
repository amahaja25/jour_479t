from playwright.sync_api import sync_playwright
import json
import os

os.makedirs("week3/data", exist_ok=True)

API_URL = "https://dbknews.com/wp-json/wp/v2/posts?per_page=10&page=1"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    # Visit the site first to establish context
    page.goto("https://dbknews.com", timeout=60000)

    # Fetch API data *inside the browser*
    data = page.evaluate(
        """async (url) => {
            const response = await fetch(url, {
                credentials: 'same-origin'
            });
            return await response.json();
        }""",
        API_URL
    )

    browser.close()

with open("week3/data/dbk_api_posts.json", "w") as f:
    json.dump(data, f, indent=2)

print(f"Saved {len(data)} posts")
