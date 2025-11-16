from sodapy import Socrata
import pandas as pd

from src.config import (
    NYC_SOCRATA_DOMAIN,
    NYC_EVENTS_DATASET_ID,
    EVENTS_START,
    EVENTS_END,
    EVENTS_RAW_DIR,
)


def fetch_events_raw() -> pd.DataFrame:
    client = Socrata(NYC_SOCRATA_DOMAIN, None)  # unauthenticated
    print(f"[INFO] Fetching events from {EVENTS_START} to {EVENTS_END}")

    results = client.get(
        NYC_EVENTS_DATASET_ID,
        where=(
            f"start_date_time >= '{EVENTS_START}' AND "
            f"start_date_time < '{EVENTS_END}'"
        ),
        limit=5_000_000,
    )

    df = pd.DataFrame.from_records(results)
    return df


def save_events_raw():
    df = fetch_events_raw()

    if "start_date_time" not in df.columns:
        raise RuntimeError("Column 'start_date_time' missing in events dataset")
    if "end_date_time" not in df.columns:
        df["end_date_time"] = df["start_date_time"]

    EVENTS_RAW_DIR.mkdir(parents=True, exist_ok=True)
    path = EVENTS_RAW_DIR / "events_2015_2024_raw.csv"
    df.to_csv(path, index=False)
    print(f"[INFO] Saved raw events to {path}")


if __name__ == "__main__":
    save_events_raw()
