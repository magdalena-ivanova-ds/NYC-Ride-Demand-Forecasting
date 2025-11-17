import pandas as pd
from src.config import EVENTS_RAW_DIR, EVENTS_HOURLY_PATH, PROCESSED_DIR

def load_raw_events():
    path = EVENTS_RAW_DIR / "events_2015_2024_raw.csv"
    df = pd.read_csv(path)

    df["start_date_time"] = pd.to_datetime(df["start_date_time"])
    df["end_date_time"] = pd.to_datetime(df["end_date_time"])
    df["end_date_time"] = df["end_date_time"].fillna(df["start_date_time"])

    return df


def build_hourly_events(df_raw):
    # Create full hourly index
    hourly = pd.DataFrame({
        "timestamp": pd.date_range(
            start="2015-01-01",
            end="2024-12-31 23:00:00",
            freq="h"
        )
    })

    hourly["event_count"] = 0

    # Convert to numpy for speed
    ts = hourly["timestamp"].values

    starts = df_raw["start_date_time"].values
    ends = df_raw["end_date_time"].values

    # Vectorized expansion using broadcasting
    for start, end in zip(starts, ends):
        mask = (ts >= start) & (ts <= end)
        hourly.loc[mask, "event_count"] += 1

    hourly["has_event"] = (hourly["event_count"] > 0).astype(int)
    return hourly


def build_and_save_hourly_events():
    print("[INFO] Loading raw events")
    df_raw = load_raw_events()

    print("[INFO] Building hourly events (vectorized fast)")
    hourly = build_hourly_events(df_raw)

    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    hourly.to_parquet(EVENTS_HOURLY_PATH, index=False)
    print(f"[INFO] Saved hourly events to {EVENTS_HOURLY_PATH}")


if __name__ == "__main__":
    build_and_save_hourly_events()

