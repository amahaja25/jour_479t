import requests 
import json
import os

cns_url = "https://dbknews.com/wp-json/wp/v2/posts"
cns_filename = "week3/data/dbk_stories.json"

# Create data folder if it doesn't exist
os.makedirs("week3/data", exist_ok=True)

# Add headers to avoid being blocked by the server
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    "Accept": "application/json,text/html;q=0.9,*/*;q=0.8",
    "Referer": "https://dbknews.com/",
}


all_posts = []
page = 1
per_page = 100
max_pages = 10

while page <= max_pages:
    params = {"per_page": per_page, "page": page}
    try:
        response = requests.get(cns_url, headers=headers, params=params, timeout=15)
    except requests.exceptions.RequestException as exc:
        print(f"Error: Network request failed for {cns_url}")
        print(f"Details: {exc}")
        break

    print(f"Status code (page {page}): {response.status_code}")

    if response.status_code != 200:
        print(f"Error: Failed to fetch data from {cns_url}")
        print(f"Response: {response.text[:200]}")
        break

    try:
        data = response.json()
    except json.JSONDecodeError:
        print("Error: Response is not valid JSON")
        print(f"Response text: {response.text[:200]}")
        break

    if not data:
        break

    all_posts.extend(data)
    page += 1

if all_posts:
    with open(cns_filename, "w") as f:
        json.dump(all_posts, f, indent=4)
    print(f"Saved {len(all_posts)} posts to {cns_filename}")
