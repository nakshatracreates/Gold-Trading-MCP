
import pandas as pd

# 1. Load historical gold data
df = pd.read_csv("XAUUSD_M1.csv")

# 2. Calculate moving averages
df["SMA_20"] = df["close"].rolling(window=20).mean()
df["SMA_50"] = df["close"].rolling(window=50).mean()

# 3. Generate crossover signals
df["Signal"] = 0

buy_condition = (
    (df["SMA_20"] > df["SMA_50"]) &
    (df["SMA_20"].shift(1) <= df["SMA_50"].shift(1))
)

sell_condition = (
    (df["SMA_20"] < df["SMA_50"]) &
    (df["SMA_20"].shift(1) >= df["SMA_50"].shift(1))
)

df.loc[buy_condition, "Signal"] = 1
df.loc[sell_condition, "Signal"] = -1

# 4. Backtesting configuration
initial_balance = 10000
balance = initial_balance

# Assumed cost in price units per completed trade.
# Replace this with measured broker costs before trusting results.
cost_per_trade = 0.0

position = 0
entry_price = 0.0
entry_time = None

trades = []

# 5. Simulate trades
for i in range(len(df) - 1):

    signal = int(df.iloc[i]["Signal"])
    next_open = float(df.iloc[i + 1]["open"])
    next_time = df.iloc[i + 1]["time"]

    if signal == 0:
        continue

    # Close the existing position
    if position != 0:

        if position == 1:
            gross_pnl = next_open - entry_price
            trade_type = "BUY"
        else:
            gross_pnl = entry_price - next_open
            trade_type = "SELL"

        net_pnl = gross_pnl - cost_per_trade
        balance += net_pnl

        trades.append({
            "Type": trade_type,
            "Entry_Time": entry_time,
            "Exit_Time": next_time,
            "Entry_Price": entry_price,
            "Exit_Price": next_open,
            "Gross_PnL": gross_pnl,
            "Cost": cost_per_trade,
            "Net_PnL": net_pnl,
            "Balance": balance
        })

    # Open the new position
    position = signal
    entry_price = next_open
    entry_time = next_time

# 6. Close any remaining position at the final candle
if position != 0:

    final_price = float(df.iloc[-1]["close"])
    final_time = df.iloc[-1]["time"]

    if position == 1:
        gross_pnl = final_price - entry_price
        trade_type = "BUY"
    else:
        gross_pnl = entry_price - final_price
        trade_type = "SELL"

    net_pnl = gross_pnl - cost_per_trade
    balance += net_pnl

    trades.append({
        "Type": trade_type,
        "Entry_Time": entry_time,
        "Exit_Time": final_time,
        "Entry_Price": entry_price,
        "Exit_Price": final_price,
        "Gross_PnL": gross_pnl,
        "Cost": cost_per_trade,
        "Net_PnL": net_pnl,
        "Balance": balance
    })

# 7. Calculate performance metrics
trades_df = pd.DataFrame(trades)

if not trades_df.empty:

    total_trades = len(trades_df)
    winning_trades = (trades_df["Net_PnL"] > 0).sum()
    losing_trades = (trades_df["Net_PnL"] < 0).sum()

    win_rate = winning_trades / total_trades * 100

    gross_profit = trades_df.loc[
        trades_df["Net_PnL"] > 0, "Net_PnL"
    ].sum()

    gross_loss = abs(trades_df.loc[
        trades_df["Net_PnL"] < 0, "Net_PnL"
    ].sum())

    profit_factor = (
        gross_profit / gross_loss if gross_loss > 0 else float("inf")
    )

    # Trade-level balance drawdown
    equity = pd.Series(
        [initial_balance] + trades_df["Balance"].tolist()
    )
    peak = equity.cummax()
    drawdown = (peak - equity) / peak * 100
    max_drawdown = drawdown.max()

    # 8. Display results
    print("\nTRADE HISTORY")
    print(trades_df.to_string(index=False))

    print("\nBACKTEST SUMMARY")
    print("Initial Balance:", initial_balance)
    print("Final Balance:", round(balance, 2))
    print("Net PnL:", round(balance - initial_balance, 2))
    print("Total Trades:", total_trades)
    print("Winning Trades:", winning_trades)
    print("Losing Trades:", losing_trades)
    print("Win Rate:", round(win_rate, 2), "%")
    print("Profit Factor:", round(profit_factor, 2))
    print("Maximum Drawdown:", round(max_drawdown, 2), "%")

else:
    print("No completed trades found.")

df.to_csv("backtest_data.csv", index=False)
trades_df.to_csv("trade_history.csv", index=False)

print("Backtest files saved successfully.")
