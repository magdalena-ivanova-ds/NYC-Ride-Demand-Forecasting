import pandas as pd
import holidays

from src.config import (
    TAXI_HOURLY_PATH,
    WEATHER_HOURLY_PATH,
    EVENTS_HOURLY_PATH,
    BASE_TABLE_PATH,
    PROCESSED_DIR,
)
from src.utils.time_utils import merge_on_timestamp


def add_calendar_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["year"] = df["timestamp"].dt.year
    df["month"] = df["timestamp"].dt.month
    df["day"] = df["timestamp"].dt.day
    df["hour"] = df["timestamp"].dt.hour
    df["dayofweek"] = df["timestamp"].dt.dayofweek
    df["is_weekend"] = df["dayofweek"].isin([5, 6]).astype(int)

    us_holidays = holidays.US()
    df["date"] = df["timestamp"].dt.date
    df["is_holiday"] = df["date"].apply(lambda d: int(d in us_holidays))
    df = df.drop(columns=["date"])
    return df


def build_base_table():
    print("[INFO] Loading hourly taxi data")
    taxi = pd.read_parquet(TAXI_HOURLY_PATH)
    taxi["timestamp"] = pd.to_datetime(taxi["timestamp"])

    print("[INFO] Loading hourly weather data")
    weather = pd.read_parquet(WEATHER_HOURLY_PATH)
    weather["timestamp"] = pd.to_datetime(weather["timestamp"])

    print("[INFO] Loading hourly events data")
    events = pd.read_parquet(EVENTS_HOURLY_PATH)
    events["timestamp"] = pd.to_datetime(events["timestamp"])

    df = taxi.sort_values("timestamp")
    df = merge_on_timestamp(df, weather, how="left")
    df = merge_on_timestamp(df, events, how="left")

    if "event_count" in df.columns:
        df["event_count"] = df["event_count"].fillna(0)
    if "has_event" in df.columns:
        df["has_event"] = df["has_event"].fillna(0)

    df = add_calendar_features(df)

    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    df.to_parquet(BASE_TABLE_PATH, index=False)
    print(f"[INFO] Saved base hourly table to {BASE_TABLE_PATH}")


if __name__ == "__main__":
    build_base_table()
