import requests 
import json
import os

cns_url = "https://cnsmaryland.org/wp-json/wp/v2/posts"
cns_filename = "week3/data/cns_stories.json"

# Create data folder if it doesn't exist
os.makedirs("week3/data", exist_ok=True)

# Add headers to avoid being blocked by the server
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}


all_posts = []
page = 1
per_page = 100
max_pages = 10

while page <= max_pages:
    params = {"per_page": per_page, "page": page}
    response = requests.get(cns_url, headers=headers, params=params)
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
