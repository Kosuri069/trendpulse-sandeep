import os
import pandas as pd

DATA_DIR = "data"
CLEAN_FILE = os.path.join(DATA_DIR, "cleaned_hn_stories.csv")
AUTHOR_FILE = os.path.join(DATA_DIR, "top_authors.csv")
DOMAIN_FILE = os.path.join(DATA_DIR, "top_domains.csv")
SUMMARY_FILE = os.path.join(DATA_DIR, "analysis_summary.txt")


def main():
    df = pd.read_csv(CLEAN_FILE)

    top_authors = (
        df.groupby("by", as_index=False)
        .agg(
            stories=("id", "count"),
            total_score=("score", "sum"),
            avg_score=("score", "mean"),
        )
        .sort_values(["stories", "total_score"], ascending=[False, False])
        .head(10)
    )

    top_domains = (
        df.groupby("domain", as_index=False)
        .agg(
            stories=("id", "count"),
            total_score=("score", "sum"),
            avg_comments=("descendants", "mean"),
        )
        .sort_values(["stories", "total_score"], ascending=[False, False])
        .head(10)
    )

    score_stats = df["score"].describe()
    comment_stats = df["descendants"].describe()
    hour_counts = df["published_hour_utc"].value_counts().sort_index()

    top_authors.to_csv(AUTHOR_FILE, index=False)
    top_domains.to_csv(DOMAIN_FILE, index=False)

    with open(SUMMARY_FILE, "w", encoding="utf-8") as f:
        f.write("Hacker News TrendPulse Analysis\n")
        f.write("=" * 40 + "\n\n")

        f.write(f"Total stories analyzed: {len(df)}\n\n")

        f.write("Score statistics:\n")
        f.write(score_stats.to_string())
        f.write("\n\n")

        f.write("Comment statistics:\n")
        f.write(comment_stats.to_string())
        f.write("\n\n")

        f.write("Top authors:\n")
        f.write(top_authors.to_string(index=False))
        f.write("\n\n")

        f.write("Top domains:\n")
        f.write(top_domains.to_string(index=False))
        f.write("\n\n")

        f.write("Stories by publishing hour (UTC):\n")
        f.write(hour_counts.to_string())
        f.write("\n")

    print("Analysis complete.")
    print("\nTop Authors:\n", top_authors)
    print("\nTop Domains:\n", top_domains)


if __name__ == "__main__":
    main()