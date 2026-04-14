import os
import glob
import pandas as pd


DATA_FOLDER = "data"


def get_latest_json_file():
    """Return the most recent trends JSON file from the data folder."""
    pattern = os.path.join(DATA_FOLDER, "trends_*.json")
    files = glob.glob(pattern)

    if not files:
        raise FileNotFoundError("No trends JSON file found in data/ folder.")

    return max(files, key=os.path.getmtime)


def main():
    input_file = get_latest_json_file()

    df = pd.read_json(input_file)

    # Remove duplicate posts by unique post_id
    df = df.drop_duplicates(subset=["post_id"]).copy()

    # Standardize text fields
    df["title"] = df["title"].fillna("").str.strip()
    df["category"] = df["category"].fillna("").str.strip().str.lower()
    df["author"] = df["author"].fillna("unknown").str.strip().str.lower()

    # Convert numeric columns safely
    df["score"] = pd.to_numeric(df["score"], errors="coerce").fillna(0).astype(int)
    df["num_comments"] = pd.to_numeric(df["num_comments"], errors="coerce").fillna(0).astype(int)

    # Convert collected_at to datetime
    df["collected_at"] = pd.to_datetime(df["collected_at"], errors="coerce")

    # Remove rows with missing important fields
    df = df[df["post_id"].notna()]
    df = df[df["title"] != ""]
    df = df[df["category"] != ""]

    # Sort by category and score
    df = df.sort_values(by=["category", "score"], ascending=[True, False])

    output_file = os.path.join(DATA_FOLDER, "cleaned_trends.csv")
    df.to_csv(output_file, index=False)

    print(f"Cleaned {len(df)} records. Saved to {output_file}")


if __name__ == "__main__":
    main()