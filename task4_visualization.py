import os
import matplotlib.pyplot as plt
import pandas as pd


DATA_FOLDER = "data"
OUTPUT_FOLDER = "outputs"


def main():
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    cleaned_file = os.path.join(DATA_FOLDER, "cleaned_trends.csv")
    category_file = os.path.join(DATA_FOLDER, "category_summary.csv")
    authors_file = os.path.join(DATA_FOLDER, "top_authors.csv")

    df = pd.read_csv(cleaned_file)
    category_summary = pd.read_csv(category_file)
    top_authors = pd.read_csv(authors_file)

    # Chart 1: Number of posts by category
    plt.figure(figsize=(8, 5))
    plt.bar(category_summary["category"], category_summary["total_posts"])
    plt.title("Number of Trending Stories by Category")
    plt.xlabel("Category")
    plt.ylabel("Total Posts")
    plt.xticks(rotation=30)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_FOLDER, "posts_by_category.png"))
    plt.close()

    # Chart 2: Average score by category
    plt.figure(figsize=(8, 5))
    plt.bar(category_summary["category"], category_summary["avg_score"])
    plt.title("Average Score by Category")
    plt.xlabel("Category")
    plt.ylabel("Average Score")
    plt.xticks(rotation=30)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_FOLDER, "avg_score_by_category.png"))
    plt.close()

    # Chart 3: Top authors by number of posts
    plt.figure(figsize=(10, 5))
    plt.bar(top_authors["author"], top_authors["total_posts"])
    plt.title("Top Authors by Number of Posts")
    plt.xlabel("Author")
    plt.ylabel("Total Posts")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_FOLDER, "top_authors.png"))
    plt.close()

    # Chart 4: Score distribution
    plt.figure(figsize=(8, 5))
    plt.hist(df["score"], bins=20)
    plt.title("Distribution of Story Scores")
    plt.xlabel("Score")
    plt.ylabel("Frequency")
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_FOLDER, "score_distribution.png"))
    plt.close()

    print(f"Visualizations saved in {OUTPUT_FOLDER}/")


if __name__ == "__main__":
    main()