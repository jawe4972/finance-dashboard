"""
Very small, transparent forecasting helper.
For a production system you might switch to Prophet,
ARIMA, or an LSTM, but a rolling 30-day exponential
smoothing keeps dependencies light and still
demonstrates the predictive capability.
"""
import pandas as pd
from .models import Expense
from . import db
from datetime import timedelta, date

def forecast_cashflow(user_id, horizon=30):
    # ---- Historical daily net-cash-flow --------------------------
    q = Expense.query.filter_by(user_id=user_id).all()
    if not q:     # no data -> return zeros
        idx = pd.date_range(date.today(), periods=horizon, freq="D")
        return pd.DataFrame({"date": idx, "prediction": 0.0})

    df = pd.DataFrame(
        [(e.date, e.amount) for e in q], columns=["date", "amount"]
    ).groupby("date").sum().asfreq("D", fill_value=0)

    # ---- Simple forecasting  ------------------------------------
    # 1. Exponential smoothing
    alpha = 0.3
    forecast = [df["amount"].iloc[-1]]
    for _ in range(1, horizon):
        next_val = alpha * forecast[-1] + (1 - alpha) * forecast[-1]
        forecast.append(next_val)

    dates = pd.date_range(df.index[-1] + timedelta(days=1), periods=horizon)
    out = pd.DataFrame({"date": dates, "prediction": forecast})
    return out
