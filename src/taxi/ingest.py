import pandas as pd
import requests
from io import BytesIO

from src.config import START_YEAR_TAXI, END_YEAR_TAXI, TAXI_HOURLY_PATH, PROCESSED_DIR

BASE_URL = "https://d37ci6vzurychx.cloudfront.net/trip-data"


def build_taxi_url(year: int, month: int) -> str:
    return f"{BASE_URL}/yellow_tripdata_{year}-{month:02d}.parquet"


def load_month_remote(year: int, month: int):
    """
    Download a single month of yellow taxi data from TLC CloudFront directly into memory,
    aggregate to hourly, and return a small DataFrame. Returns None if missing.
    """
    url = build_taxi_url(year, month)
    print(f"[INFO] Fetching {url}")

    try:
        r = requests.get(url, timeout=60)
    except requests.RequestException as e:
        print(f"[ERROR] Request failed for {url}: {e}")
        return None

    if r.status_code == 404:
        print(f"[WARN] 404 Not Found: {url}")
        return None

    r.raise_for_status()

    bio = BytesIO(r.content)
    try:
        df = pd.read_parquet(bio, columns=["tpep_pickup_datetime"])
    except Exception as e:
        print(f"[ERROR] Failed to read parquet for {url}: {e}")
        return None

    df["pickup_datetime"] = pd.to_datetime(df["tpep_pickup_datetime"])
    df["timestamp"] = df["pickup_datetime"].dt.floor("H")

    hourly = (
        df.groupby("timestamp")
          .size()
          .reset_index(name="rides")
    )
    return hourly


def load_year_hourly(year: int) -> pd.DataFrame:
    monthly_hourly = []

    for month in range(1, 13):
        h = load_month_remote(year, month)
        if h is not None and not h.empty:
            monthly_hourly.append(h)

    if not monthly_hourly:
        print(f"[WARN] No hourly data for year {year}")
        return pd.DataFrame(columns=["timestamp", "rides"])

    year_hourly = pd.concat(monthly_hourly, ignore_index=True)
    year_hourly = (
        year_hourly.groupby("timestamp", as_index=False)["rides"]
        .sum()
        .sort_values("timestamp")
    )
    return year_hourly


def build_full_hourly():
    """
    Build the full 2015–2024 hourly demand table by streaming each month from TLC.
    No raw parquet is stored on disk. Only the final aggregated table is saved.
    """
    all_years = []

    for year in range(START_YEAR_TAXI, END_YEAR_TAXI + 1):
        print(f"[INFO] Aggregating taxi data for year {year}")
        year_hourly = load_year_hourly(year)
        if not year_hourly.empty:
            all_years.append(year_hourly)

    if not all_years:
        raise RuntimeError("No taxi data loaded at all. Check years and URLs.")

    full = pd.concat(all_years, ignore_index=True)
    full = (
        full.groupby("timestamp", as_index=False)["rides"]
        .sum()
        .sort_values("timestamp")
    )

    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    full.to_parquet(TAXI_HOURLY_PATH, index=False)
    print(f"[INFO] Saved hourly taxi demand to {TAXI_HOURLY_PATH}")


if __name__ == "__main__":
    build_full_hourly()
