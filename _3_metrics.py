import numpy as np
import pandas as pd

def weekday_metrics(df):
    wdf = df[["dollar_exchange_rate", "day_name"]].copy()

    wdf["log_returns"] = (
        np.log(wdf["dollar_exchange_rate"])
        - np.log(wdf["dollar_exchange_rate"].shift(1))
    )

    wdf = (
        wdf
        .dropna(subset=["log_returns"])
        .groupby("day_name", as_index=False)
        .agg(
            n_days=("log_returns", "count"),
            avg_return=("log_returns", "mean"),
            volatility=("log_returns", "std"),
            pct_positive_days=("log_returns", lambda x: (x > 0).mean())
        )
    )

    wdf["t_stat"] = (
        wdf["avg_return"]
        / (wdf["volatility"] / np.sqrt(wdf["n_days"]))
    )

    return wdf
