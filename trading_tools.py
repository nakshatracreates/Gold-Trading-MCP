from pydantic import Field,validate_call,ValidationError
from typing import Annotated

@validate_call
def calculate_risk_amount(balance:Annotated[float,Field(gt=0)],risk_percentage:Annotated[int,Field(le=100,gt=0)]):
        risk_amount=balance*risk_percentage/100
        return risk_amount

@validate_call
def calculate_position_size(risk_amount:Annotated[float,Field(gt=0)],stop_loss_distance:Annotated[float,Field(gt=0)],value_per_dollar_per_lot:Annotated[float,Field(gt=0)]):
    
    loss_per_lot=stop_loss_distance*value_per_dollar_per_lot
    lot_size=risk_amount/loss_per_lot
    return lot_size

import pandas as pd


def get_gold_data():
    """Retrieve the latest 100 XAUUSD candles."""
    df = pd.read_csv("XAUUSD_M1.csv")
    return df.tail(100).to_dict(orient="records")


def get_backtest_results():
    """Retrieve the saved SMA backtest trade history."""
    df = pd.read_csv("trade_history.csv")
    return df.to_dict(orient="records")


def run_sma_backtest(days: int):
    """Return SMA backtest performance for the specified number of days."""

    df = pd.read_csv("trade_history.csv")

    if df.empty:
        return {"message": "No backtest trades available."}

    # Convert exit time into datetime
    df["Exit_Time"] = pd.to_datetime(df["Exit_Time"])

    # Find the latest date in the dataset
    end_date = df["Exit_Time"].max()

    # Calculate the starting date
    start_date = end_date - pd.Timedelta(days=days)

    # Filter trades within the requested period
    df = df[
        (df["Exit_Time"] > start_date) &
        (df["Exit_Time"] <= end_date)
    ]

    if df.empty:
        return {"message": f"No trades found in the last {days} days."}

    initial_balance = 10000
    net_pnl = float(df["Net_PnL"].sum())
    final_balance = initial_balance + net_pnl

    total_trades = len(df)
    winning_trades = int((df["Net_PnL"] > 0).sum())
    losing_trades = int((df["Net_PnL"] < 0).sum())

    gross_profit = df.loc[df["Net_PnL"] > 0, "Net_PnL"].sum()
    gross_loss = abs(df.loc[df["Net_PnL"] < 0, "Net_PnL"].sum())

    return {
        "period_days": days,
        "start_date": str(start_date),
        "end_date": str(end_date),
        "initial_balance": initial_balance,
        "final_balance": round(final_balance, 2),
        "net_pnl": round(net_pnl, 2),
        "total_trades": total_trades,
        "winning_trades": winning_trades,
        "losing_trades": losing_trades,
        "win_rate": round(winning_trades / total_trades * 100, 2),
        "profit_factor": round(gross_profit / gross_loss, 2) if gross_loss else None
    }
