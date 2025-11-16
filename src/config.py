from pathlib import Path

# Base paths
BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"

RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"

# Raw dirs (only events/weather if you want to store raw)
WEATHER_RAW_DIR = RAW_DIR / "weather"
EVENTS_RAW_DIR = RAW_DIR / "events_raw"

# Processed files
TAXI_HOURLY_PATH = PROCESSED_DIR / "hourly_taxi_2015_2024.parquet"
WEATHER_HOURLY_PATH = PROCESSED_DIR / "hourly_weather_2015_2024.parquet"
EVENTS_HOURLY_PATH = PROCESSED_DIR / "hourly_events_2015_2025.parquet"
BASE_TABLE_PATH = PROCESSED_DIR / "base_hourly_2015_2024.parquet"

# Taxi years
START_YEAR_TAXI = 2015
END_YEAR_TAXI = 2024  # inclusive

# Weather range
WEATHER_START_DATE = "2015-01-01"
WEATHER_END_DATE = "2024-12-31"

# Events range
EVENTS_START = "2015-01-01T00:00:00"
EVENTS_END = "2025-01-01T00:00:00"

# NYC coords / timezone
NYC_LAT = 40.7128
NYC_LON = -74.0060
NYC_TIMEZONE = "America/New_York"

# NYC Open Data
NYC_SOCRATA_DOMAIN = "data.cityofnewyork.us"
NYC_EVENTS_DATASET_ID = "bkfu-528j"
