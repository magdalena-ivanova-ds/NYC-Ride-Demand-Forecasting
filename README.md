# NYC Ride Demand Forecasting (2015–2024)

Forecast hourly NYC yellow cab demand using:
- 10 years of taxi trip records (TLC Parquet)
- 10 years of hourly weather (Open-Meteo ERA5)
- 10 years of official NYC permitted events (Socrata API)

## Data flow

1. **Taxi**
   - Load monthly Parquet files from TLC
   - Aggregate to hourly demand: `timestamp, rides`

2. **Weather**
   - Pull ERA5 hourly data (Open-Meteo) for NYC
   - Save as `timestamp + weather features`

3. **Events**
   - Pull events from NYC Open Data (`bkfu-528j`)
   - Expand to hourly based on `start_date_time` → `end_date_time`
   - Aggregate per hour: `event_count`, `has_event`

4. **Base Table**
   - Merge taxi, weather, and events by `timestamp`
   - Output: `data/processed/base_hourly.parquet` (for modeling)

## Setup

```bash
pip install -r requirements.txt
