import importlib
from clean_watch_history import clean_watch_history
from generate_data import main as generate_data


def run_pipeline():
    print("=" * 40)
    print("PIPELINE START")
    print("=" * 40)

    print("\n[1/2] Generating raw data...")
    generate_data()

    print("\n[2/2] Cleaning watch history...")
    clean_watch_history()

    print("\n" + "=" * 40)
    print("PIPELINE COMPLETE")
    print("=" * 40)


if __name__ == "__main__":
    run_pipeline()
