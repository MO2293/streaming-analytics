import os
import numpy as np
import pandas as pd

RNG_SEED = 42
rng = np.random.default_rng(RNG_SEED)

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DIR = os.path.join(PROJECT_ROOT, "data", "raw")
os.makedirs(RAW_DIR, exist_ok=True)


def generate_titles(n_titles: int = 500) -> pd.DataFrame:
    genres = [
        "Drama", "Comedy", "Action", "Thriller", "Romance",
        "Sci-Fi", "Fantasy", "Horror", "Documentary", "Animation",
    ]
    content_ratings = ["G", "PG", "PG-13", "R", "TV-14", "TV-MA"]
    formats = ["Movie", "Series"]

    title_ids = np.arange(1, n_titles + 1)

    df = pd.DataFrame({
        "title_id": title_ids,
        "title_name": [f"Title {i}" for i in title_ids],
        "primary_genre": rng.choice(genres, size=n_titles),
        "release_year": rng.integers(1980, 2024, size=n_titles),
        "content_rating": rng.choice(content_ratings, size=n_titles),
        "format": rng.choice(formats, size=n_titles, p=[0.7, 0.3]),
        "duration_minutes": rng.integers(60, 140, size=n_titles),
        "is_original": rng.choice([0, 1], size=n_titles, p=[0.7, 0.3]),
    })
    return df

def generate_users(n_users: int = 2000) -> pd.DataFrame:
    """Generate a synthetic user base with realistic signup dates."""
    countries = ["CA", "US", "UK", "DE", "FR", "IN", "BR", "AU"]
    plans = ["Basic", "Standard", "Premium"]

    user_ids = np.arange(1, n_users + 1)

    # Signup dates between 2017-01-01 and 2024-01-01
    signup_start = pd.Timestamp("2017-01-01")
    signup_end = pd.Timestamp("2024-01-01")
    total_days = (signup_end - signup_start).days

    signup_dates = signup_start + pd.to_timedelta(
        rng.integers(0, total_days, size=n_users),
        unit="D"
    )

    df = pd.DataFrame({
        "user_id": user_ids,
        "country": rng.choice(countries, size=n_users),
        "subscription_plan": rng.choice(plans, size=n_users, p=[0.4, 0.4, 0.2]),
        "signup_date": signup_dates,
    })
    return df



def generate_watch_history(
    users: pd.DataFrame,
    titles: pd.DataFrame,
    avg_events_per_user: int = 25,
) -> pd.DataFrame:
    devices = ["Mobile", "TV", "Web", "Tablet"]

    n_users = len(users)
    n_events = n_users * avg_events_per_user

    user_ids = rng.choice(users["user_id"].values, size=n_events)
    title_ids = rng.choice(titles["title_id"].values, size=n_events)

    # Dates between 2022-01-01 and 2024-12-31
    start = pd.Timestamp("2022-01-01")
    end = pd.Timestamp("2024-12-31")
    days = (end - start).days
    watch_dates = start + pd.to_timedelta(
        rng.integers(0, days, size=n_events), unit="D"
    )

    watch_hour = rng.integers(0, 24, size=n_events)
    device_type = rng.choice(devices, size=n_events, p=[0.4, 0.4, 0.15, 0.05])
    minutes_watched = rng.integers(5, 180, size=n_events)

    durations = titles.set_index("title_id")["duration_minutes"]
    duration_lookup = durations.reindex(title_ids).values
    completed = (minutes_watched >= 0.7 * duration_lookup).astype(int)

    df = pd.DataFrame({
        "event_id": np.arange(1, n_events + 1),
        "user_id": user_ids,
        "title_id": title_ids,
        "watch_date": watch_dates,
        "watch_hour": watch_hour,
        "device_type": device_type,
        "minutes_watched": minutes_watched,
        "completed": completed,
    })
    return df


def main():
    print("Generating titles...")
    titles = generate_titles()
    print("Generating users...")
    users = generate_users()
    print("Generating watch history...")
    watch_history = generate_watch_history(users, titles)

    titles.to_csv(os.path.join(RAW_DIR, "titles.csv"), index=False)
    users.to_csv(os.path.join(RAW_DIR, "users.csv"), index=False)
    watch_history.to_csv(os.path.join(RAW_DIR, "watch_history.csv"), index=False)

    print("Saved:")
    print(" - data/raw/titles.csv")
    print(" - data/raw/users.csv")
    print(" - data/raw/watch_history.csv")


if __name__ == "__main__":
    main()
