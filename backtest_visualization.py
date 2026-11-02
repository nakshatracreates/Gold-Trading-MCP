import pandas as pd
import mplfinance as mpf
import matplotlib.pyplot as plt

df = pd.read_csv("backtest_data.csv")
trades = pd.read_csv("trade_history.csv")

df["time"] = pd.to_datetime(df["time"])
df.set_index("time", inplace=True)

trades["Entry_Time"] = pd.to_datetime(trades["Entry_Time"])
trades["Exit_Time"] = pd.to_datetime(trades["Exit_Time"])

df["Buy"] = float("nan")
df["Sell"] = float("nan")

for _, trade in trades.iterrows():
    entry_time = trade["Entry_Time"]

    if entry_time in df.index:
        if trade["Type"].lower() == "buy":
            df.loc[entry_time, "Buy"] = df.loc[entry_time, "low"] * 0.999
        else:
            df.loc[entry_time, "Sell"] = df.loc[entry_time, "high"] * 1.001

addplots = [
    mpf.make_addplot(df["SMA_20"]),
    mpf.make_addplot(df["SMA_50"]),
    mpf.make_addplot(df["Buy"], type="scatter", marker="^", markersize=80),
    mpf.make_addplot(df["Sell"], type="scatter", marker="v", markersize=80),
]

mpf.plot(
    df,
    type="candle",
    style="charles",
    addplot=addplots,
    volume=False,
    title="XAUUSD - SMA 20/50 Backtest",
    ylabel="Gold Price",
    figsize=(16, 8),
    savefig="backtest_chart.png"
)

plt.figure(figsize=(12, 5))
plt.plot(trades["Exit_Time"], trades["Balance"])
plt.title("Backtest Account Balance")
plt.xlabel("Date")
plt.ylabel("Balance")
plt.grid(True)
plt.tight_layout()
plt.savefig("balance_chart.png")
plt.show()

print("Charts saved successfully.")

