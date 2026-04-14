import os
import json
import time
from datetime import datetime

import requests


HEADERS = {"User-Agent": "TrendPulse/1.0"}
TOP_STORIES_URL = "https://hacker-news.firebaseio.com/v0/topstories.json"
ITEM_URL_TEMPLATE = "https://hacker-news.firebaseio.com/v0/item/{}.json"

MAX_TOP_IDS = 500
MAX_PER_CATEGORY = 25

CATEGORY_KEYWORDS = {
    "technology": [
        "ai", "software", "tech", "code", "computer",
        "data", "cloud", "api", "gpu", "llm"
    ],
    "worldnews": [
        "war", "government", "country", "president", "election",
        "climate", "attack", "global"
    ],
    "sports": [
        "nfl", "nba", "fifa", "sport", "game",
        "team", "player", "league", "championship"
    ],
    "science": [
        "research", "study", "space", "physics", "biology",
        "discovery", "nasa", "genome"
    ],
    "entertainment": [
        "movie", "film", "music", "netflix", "game",
        "book", "show", "award", "streaming"
    ],
}


def fetch_json(url):
    """Fetch JSON safely. Return None on failure."""
    try:
        response = requests.get(url, headers=HEADERS, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as exc:
        print(f"Request failed for {url}: {exc}")
        return None


def get_top_story_ids(limit=500):
    """Fetch top story IDs and return the first 'limit'."""
    story_ids = fetch_json(TOP_STORIES_URL)
    if not story_ids:
        return []
    return story_ids[:limit]


def get_story_details(story_id):
    """Fetch one story by ID."""
    url = ITEM_URL_TEMPLATE.format(story_id)
    return fetch_json(url)


def title_matches_category(title, keywords):
    """Return True if any keyword appears in the title, case-insensitive."""
    title_lower = title.lower()
    return any(keyword.lower() in title_lower for keyword in keywords)


def collect_stories():
    """
    Collect up to 25 stories per category from the first 500 top stories.
    Sleep 2 seconds once per category loop.
    """
    top_story_ids = get_top_story_ids(MAX_TOP_IDS)
    if not top_story_ids:
        print("No story IDs were fetched.")
        return []

    collected_stories = []
    collected_ids = set()

    for category, keywords in CATEGORY_KEYWORDS.items():
        category_count = 0

        for story_id in top_story_ids:
            if category_count >= MAX_PER_CATEGORY:
                break

            if story_id in collected_ids:
                continue

            story = get_story_details(story_id)
            if not story:
                continue

            if story.get("type") != "story":
                continue

            title = story.get("title")
            if not title:
                continue

            if not title_matches_category(title, keywords):
                continue

            collected_stories.append({
                "post_id": story.get("id"),
                "title": title,
                "category": category,
                "score": story.get("score", 0),
                "num_comments": story.get("descendants", 0),
                "author": story.get("by", "unknown"),
                "collected_at": datetime.now().isoformat()
            })

            collected_ids.add(story_id)
            category_count += 1

        # Required: one sleep per category loop
        time.sleep(2)

    return collected_stories


def save_to_json(stories):
    """Save collected stories to data/trends_YYYYMMDD.json."""
    os.makedirs("data", exist_ok=True)

    file_date = datetime.now().strftime("%Y%m%d")
    file_path = f"data/trends_{file_date}.json"

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(stories, file, indent=2, ensure_ascii=False)

    print(f"Collected {len(stories)} stories. Saved to {file_path}")


def main():
    stories = collect_stories()
    save_to_json(stories)


if __name__ == "__main__":
    main()