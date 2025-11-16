import requests
import pandas as pd
from src.config import (
    NYC_LAT,
    NYC_LON,
    NYC_TIMEZONE,
    WEATHER_START_DATE,
    WEATHER_END_DATE,
    WEATHER_HOURLY_PATH,
    PROCESSED_DIR,
)


def fetch_hourly_weather() -> pd.DataFrame:
    url = "https://archive-api.open-meteo.com/v1/era5"

    params = {
        "latitude": NYC_LAT,
        "longitude": NYC_LON,
        "start_date": WEATHER_START_DATE,
        "end_date": WEATHER_END_DATE,
        "hourly": ",".join(
            [
                "temperature_2m",
                "precipitation",
                "weathercode",
                "windspeed_10m",
            ]
        ),
        "timezone": NYC_TIMEZONE,
    }

    print(f"[INFO] Requesting weather data from {WEATHER_START_DATE} to {WEATHER_END_DATE}")
    r = requests.get(url, params=params, timeout=60)
    r.raise_for_status()
    data = r.json()

    hourly = data.get("hourly", {})
    if not hourly:
        raise RuntimeError("No 'hourly' field in weather API response")

    df = pd.DataFrame(hourly)
    df["timestamp"] = pd.to_datetime(df["time"])
    df = df.drop(columns=["time"])
    df = df.sort_values("timestamp")

    return df


def save_hourly_weather():
    df = fetch_hourly_weather()
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    df.to_parquet(WEATHER_HOURLY_PATH, index=False)
    print(f"[INFO] Saved hourly weather to {WEATHER_HOURLY_PATH}")


if __name__ == "__main__":
    save_hourly_weather()
