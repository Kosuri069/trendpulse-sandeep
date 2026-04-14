import os
import time
import requests
import pandas as pd

BASE_URL = "https://hacker-news.firebaseio.com/v0"
DATA_DIR = "data"
RAW_FILE = os.path.join(DATA_DIR, "raw_hn_stories.csv")

os.makedirs(DATA_DIR, exist_ok=True)


def get_top_story_ids(limit=100):
    url = f"{BASE_URL}/topstories.json"
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    return response.json()[:limit]


def get_story(story_id):
    url = f"{BASE_URL}/item/{story_id}.json"
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    return response.json()


def extract_domain(url):
    if not url:
        return None
    try:
        return url.split("//", 1)[-1].split("/", 1)[0].lower()
    except Exception:
        return None


def main():
    story_ids = get_top_story_ids(limit=100)
    records = []

    for idx, story_id in enumerate(story_ids, start=1):
        item = get_story(story_id)

        if not item or item.get("type") != "story":
            continue

        records.append(
            {
                "id": item.get("id"),
                "title": item.get("title"),
                "by": item.get("by"),
                "time": item.get("time"),
                "score": item.get("score"),
                "descendants": item.get("descendants"),
                "url": item.get("url"),
                "domain": extract_domain(item.get("url")),
                "hn_link": f"https://news.ycombinator.com/item?id={item.get('id')}",
            }
        )

        time.sleep(0.05)

    df = pd.DataFrame(records)
    df.to_csv(RAW_FILE, index=False)
    print(f"Saved {len(df)} raw stories to {RAW_FILE}")


if __name__ == "__main__":
    main()