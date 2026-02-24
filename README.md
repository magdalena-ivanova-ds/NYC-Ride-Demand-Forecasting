# NYC Ride Demand Forecasting (2015 - 2024)

A full end-to-end project forecasting hourly NYC yellow taxi demand using 10 years of trip data, weather conditions, NYC events, and rich time-based features.
Built to demonstrate real-world demand forecasting, time-series modeling, and marketplace analytics skills.

---

## Live Dashboard

Explore predictions interactively:
**[Live Dashboard](https://magdalena-ivanova-ds-nyc-ride-demand-foreca-dashboardapp-nthc9t.streamlit.app/)**

---

## Project Summary

This project analyzes and forecasts how NYC ride demand evolves with:

* Daily + weekly seasonality (commute cycles, weekend behavior)
* NYC permitted events (concerts, sports, parades)
* Weather factors (temperature, precipitation, wind)
* Calendar dynamics (holidays, weekdays, month patterns)
* Long-term structural changes, including the COVID demand collapse

The final model uses XGBoost, producing accurate and stable short-horizon forecasts.

---

## Key Insights

### Demand Behavior

* Clear two-peak weekday pattern (AM/PM commute).
* Fridays have the highest demand; Mondays the lowest.
* Events noticeably elevate ride volume.
* Weather impacts demand moderately (rain increases rides slightly).
* Summer months show lower demand than winter.
* A major structural break occurs in 2020 due to COVID.

### Model Performance

Models evaluated:

* Naive & seasonal naive
* Linear regression
* Random Forest
* XGBoost (best)

**XGBoost** captured peak timing and magnitude well, achieving low MAE/RMSE and strong generalization to unseen weeks.

More detailed analysis and visualizations are available in the modeling notebook.

---

## Notebooks

Each notebook contains visualizations, insights, and technical explanation:

* **1_eda.ipynb** - Trend, seasonality, weather, events, structural break
* **2_feature_engineering.ipynb** - Lags, rolling features, calendar encoding
* **3_modeling.ipynb** - Baselines, models, evaluation, final metrics

**Each notebook provides deeper insight and commentary.**

---

## Running the Dashboard Locally

```bash
pip install -r requirements.txt
streamlit run dashboard/app.py
```

Everything works immediately - processed data and the trained model are included.

---

## (Optional) Rebuild the Dataset From Scratch

If you want to reproduce the full data pipeline using raw TLC data + APIs:

```bash
python -m src.taxi.ingest
python -m src.weather.fetch_weather
python -m src.events.fetch_events
python -m src.events.expand_events
python -m src.features.build_base_table
python -m src.prepare_model_data
```

This regenerates the same processed files included in the repository.

