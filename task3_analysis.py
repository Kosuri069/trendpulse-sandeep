import os
import numpy as np
import pandas as pd


DATA_FOLDER = "data"


def main():
    input_file = os.path.join(DATA_FOLDER, "cleaned_trends.csv")
    df = pd.read_csv(input_file)

    # Basic category-level analysis
    category_summary = (
        df.groupby("category", as_index=False)
        .agg(
            total_posts=("post_id", "count"),
            avg_score=("score", "mean"),
            avg_comments=("num_comments", "mean"),
            max_score=("score", "max"),
            max_comments=("num_comments", "max")
        )
        .sort_values(by="total_posts", ascending=False)
    )

    # Round averages for readability
    category_summary["avg_score"] = category_summary["avg_score"].round(2)
    category_summary["avg_comments"] = category_summary["avg_comments"].round(2)

    # Top authors by number of posts
    top_authors = (
        df.groupby("author", as_index=False)
        .agg(
            total_posts=("post_id", "count"),
            total_score=("score", "sum"),
            avg_score=("score", "mean")
        )
        .sort_values(by=["total_posts", "total_score"], ascending=[False, False])
        .head(10)
    )

    top_authors["avg_score"] = top_authors["avg_score"].round(2)

    # Top stories overall
    top_stories = (
        df[["post_id", "title", "category", "author", "score", "num_comments"]]
        .sort_values(by=["score", "num_comments"], ascending=[False, False])
        .head(10)
    )

    # NumPy-based overall stats
    overall_score_mean = np.mean(df["score"])
    overall_score_median = np.median(df["score"])
    overall_comments_mean = np.mean(df["num_comments"])
    overall_comments_median = np.median(df["num_comments"])

    # Save outputs
    category_summary.to_csv(os.path.join(DATA_FOLDER, "category_summary.csv"), index=False)
    top_authors.to_csv(os.path.join(DATA_FOLDER, "top_authors.csv"), index=False)
    top_stories.to_csv(os.path.join(DATA_FOLDER, "top_stories.csv"), index=False)

    summary_file = os.path.join(DATA_FOLDER, "analysis_summary.txt")
    with open(summary_file, "w", encoding="utf-8") as file:
        file.write("TrendPulse Analysis Summary\n")
        file.write("=" * 40 + "\n\n")
        file.write(f"Total cleaned stories: {len(df)}\n")
        file.write(f"Average score: {overall_score_mean:.2f}\n")
        file.write(f"Median score: {overall_score_median:.2f}\n")
        file.write(f"Average comments: {overall_comments_mean:.2f}\n")
        file.write(f"Median comments: {overall_comments_median:.2f}\n\n")

        file.write("Category Summary:\n")
        file.write(category_summary.to_string(index=False))
        file.write("\n\n")

        file.write("Top Authors:\n")
        file.write(top_authors.to_string(index=False))
        file.write("\n\n")

        file.write("Top Stories:\n")
        file.write(top_stories.to_string(index=False))
        file.write("\n")

    print("Analysis complete.")
    print(f"Saved category summary, top authors, top stories, and analysis summary in {DATA_FOLDER}/")


if __name__ == "__main__":
    main()