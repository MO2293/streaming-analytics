import os
import pandas as pd

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DIR = os.path.join(PROJECT_ROOT, "data", "raw")
PROCESSED_DIR = os.path.join(PROJECT_ROOT, "data", "processed")
os.makedirs(PROCESSED_DIR, exist_ok=True)

RAW_WH_PATH = os.path.join(RAW_DIR, "watch_history.csv")
CLEAN_WH_PATH = os.path.join(PROCESSED_DIR, "watch_history_cleaned.csv")


def clean_watch_history():
    df = pd.read_csv(RAW_WH_PATH, parse_dates=["watch_date"])

    before = len(df)

    # Remove missing values on critical columns
    df = df.dropna(subset=["user_id", "title_id", "minutes_watched"])

    # Remove invalid watch times
    df = df[df["minutes_watched"] > 0]

    # Remove extreme outliers (> 8 hours)
    df = df[df["minutes_watched"] <= 480]

    after = len(df)
    print(f"Rows before cleaning: {before} | After: {after} | Dropped: {before - after}")

    # Add derived columns
    df["watch_year"] = df["watch_date"].dt.year
    df["watch_month"] = df["watch_date"].dt.to_period("M").astype(str)

    # Peak hour flag (6pm - 11pm)
    df["is_peak_hour"] = df["watch_hour"].between(18, 23)

    # Save cleaned dataset
    df.to_csv(CLEAN_WH_PATH, index=False)
    print(f"Cleaned dataset saved to: {CLEAN_WH_PATH}")


if __name__ == "__main__":
    clean_watch_history()
