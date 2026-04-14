import os
import pandas as pd
import matplotlib.pyplot as plt

DATA_DIR = "data"
OUTPUT_DIR = "outputs"

CLEAN_FILE = os.path.join(DATA_DIR, "cleaned_hn_stories.csv")
AUTHOR_FILE = os.path.join(DATA_DIR, "top_authors.csv")
DOMAIN_FILE = os.path.join(DATA_DIR, "top_domains.csv")

os.makedirs(OUTPUT_DIR, exist_ok=True)


def main():
    df = pd.read_csv(CLEAN_FILE)
    top_authors = pd.read_csv(AUTHOR_FILE)
    top_domains = pd.read_csv(DOMAIN_FILE)

    plt.figure(figsize=(10, 6))
    plt.bar(top_domains["domain"], top_domains["stories"])
    plt.xticks(rotation=45, ha="right")
    plt.title("Top Hacker News Domains by Story Count")
    plt.xlabel("Domain")
    plt.ylabel("Story Count")
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "top_domains.png"))
    plt.close()

    plt.figure(figsize=(10, 6))
    plt.bar(top_authors["by"], top_authors["stories"])
    plt.xticks(rotation=45, ha="right")
    plt.title("Top Hacker News Authors by Story Count")
    plt.xlabel("Author")
    plt.ylabel("Story Count")
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "top_authors.png"))
    plt.close()

    hourly_counts = df["published_hour_utc"].value_counts().sort_index()
    plt.figure(figsize=(10, 6))
    plt.plot(hourly_counts.index, hourly_counts.values, marker="o")
    plt.title("Hacker News Story Count by Publish Hour (UTC)")
    plt.xlabel("Hour of Day (UTC)")
    plt.ylabel("Number of Stories")
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "publish_hour_trend.png"))
    plt.close()

    plt.figure(figsize=(10, 6))
    plt.hist(df["score"], bins=20)
    plt.title("Distribution of Hacker News Story Scores")
    plt.xlabel("Score")
    plt.ylabel("Frequency")
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "score_distribution.png"))
    plt.close()

    print(f"Visualizations saved in {OUTPUT_DIR}/")


if __name__ == "__main__":
    main()