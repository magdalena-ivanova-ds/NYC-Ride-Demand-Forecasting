import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path
import joblib
from xgboost import XGBRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error

# Paths
DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "processed" / "model_ready_hourly.parquet"
MODEL_PATH = Path(__file__).resolve().parent.parent / "models" / "xgb_model.pkl"


# Loaders (cached)
@st.cache_data
def load_data():
    df = pd.read_parquet(DATA_PATH)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df = df.sort_values("timestamp").reset_index(drop=True)
    return df


@st.cache_resource
def load_model():
    if not MODEL_PATH.exists():
        st.error(
            f"Model file not found at {MODEL_PATH}. "
            "Train and save the XGBoost model first."
        )
        st.stop()
    model = joblib.load(MODEL_PATH)
    if not isinstance(model, XGBRegressor):
        st.warning("Loaded model is not an XGBRegressor – check your model file.")
    return model


# Feature config
TARGET_COL = "rides"
FEATURE_COLS = [
    "lag_1", "lag_24", "lag_168",
    "roll_mean_3", "roll_mean_24",
    "diff_1", "diff_24",
    "temperature_2m", "precipitation", "windspeed_10m", "is_rain",
    "event_count", "has_event", "heavy_event", "log_event_count",
    "hour", "dayofweek", "is_weekend", "is_holiday",
]


# Main App
def main():
    st.title("NYC Ride Demand – XGBoost Dashboard")
    st.write(
        "This dashboard shows how well a trained XGBoost model can predict "
        "hourly NYC yellow taxi demand for a selected time period."
    )

    df = load_data()
    model = load_model()

    min_date = df["timestamp"].min().date()
    max_date = df["timestamp"].max().date()

    st.sidebar.header("Controls")

    # Date range selector
    default_start = max_date - pd.Timedelta(days=7)
    start_date = st.sidebar.date_input(
        "Start date", value=default_start, min_value=min_date, max_value=max_date
    )
    end_date = st.sidebar.date_input(
        "End date", value=max_date, min_value=min_date, max_value=max_date
    )

    if start_date > end_date:
        st.error("Start date must be <= end date")
        st.stop()

    # Filter data
    mask = (df["timestamp"].dt.date >= start_date) & (df["timestamp"].dt.date <= end_date)
    df_range = df[mask].copy()

    if df_range.empty:
        st.warning("No data in this range. Try a different period.")
        st.stop()

    # Predict using XGBoost for this range
    X = df_range[FEATURE_COLS].values
    y_true = df_range[TARGET_COL].values
    y_pred = model.predict(X)

    df_range["y_true"] = y_true
    df_range["y_pred"] = y_pred

    # Metrics
    mae = mean_absolute_error(y_true, y_pred)
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    mape = (np.abs((y_true - y_pred) / np.where(y_true == 0, 1, y_true))).mean() * 100

    st.subheader("Metrics for Selected Period")

    col1, col2, col3 = st.columns(3)
    col1.metric("MAE", f"{mae:,.2f}")
    col2.metric("RMSE", f"{rmse:,.2f}")
    col3.metric("MAPE", f"{mape:,.2f}%")

    # Short explanations for non-technical users
    st.markdown(
        """
**How to read these metrics:**

- **MAE (Mean Absolute Error):**  
  On average, the model is off by this many rides per hour. Lower is better.

- **RMSE (Root Mean Squared Error):**  
  Like MAE, but penalises large mistakes more strongly. Also in rides per hour.

- **MAPE (Mean Absolute Percentage Error):**  
  Average error as a percentage of the true demand. For example, 10% means the
  model is off by about 10% on average.
"""
    )

    # Table: Actual vs Predicted
    st.subheader("Table: Actual vs Predicted Rides")

    table_df = df_range[["timestamp", "y_true", "y_pred"]].copy()
    table_df = table_df.rename(
        columns={
            "timestamp": "Timestamp",
            "y_true": "Actual rides",
            "y_pred": "Predicted rides",
        }
    )
    st.dataframe(
        table_df.reset_index(drop=True),
        use_container_width=True,
    )

    # Line chart
    st.subheader("Hourly Demand: Actual vs XGBoost Prediction")

    st.write(
        "The chart below compares the true hourly demand to the model’s predictions "
        "for the selected date range."
    )

    st.line_chart(
        df_range.set_index("timestamp")[["y_true", "y_pred"]],
        height=350,
    )


if __name__ == "__main__":
    main()
