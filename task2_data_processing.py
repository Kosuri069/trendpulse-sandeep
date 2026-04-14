import os
import pandas as pd

DATA_DIR = "data"
RAW_FILE = os.path.join(DATA_DIR, "raw_hn_stories.csv")
CLEAN_FILE = os.path.join(DATA_DIR, "cleaned_hn_stories.csv")

os.makedirs(DATA_DIR, exist_ok=True)


def main():
    df = pd.read_csv(RAW_FILE)

    df = df.drop_duplicates(subset=["id"]).copy()

    df["title"] = df["title"].fillna("").str.strip()
    df["by"] = df["by"].fillna("unknown").str.strip().str.lower()
    df["domain"] = df["domain"].fillna("news.ycombinator.com").str.lower()

    numeric_cols = ["score", "descendants", "time"]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    df["published_at"] = pd.to_datetime(df["time"], unit="s", utc=True)
    df["published_date"] = df["published_at"].dt.date.astype(str)
    df["published_hour_utc"] = df["published_at"].dt.hour

    df = df[df["title"] != ""]
    df = df.sort_values(by=["score", "descendants"], ascending=[False, False])

    df.to_csv(CLEAN_FILE, index=False)
    print(f"Saved {len(df)} cleaned stories to {CLEAN_FILE}")


if __name__ == "__main__":
    main()