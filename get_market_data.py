
import MetaTrader5 as mt5
import pandas as pd
from datetime import datetime, timedelta, timezone


SYMBOL = "XAUUSDm"
TIMEFRAME = mt5.TIMEFRAME_M1
DAYS = 30
OUTPUT_FILE = "XAUUSD_M1.csv"


def get_market_data():

    
    if not mt5.initialize():
        raise RuntimeError(f"MT5 connection failed: {mt5.last_error()}")

    try:
        
        if not mt5.symbol_select(SYMBOL, True):
            raise RuntimeError(
                f"Could not select {SYMBOL}: {mt5.last_error()}"
            )

        
        end = datetime.now(timezone.utc).replace(tzinfo=None)
        start = end - timedelta(days=DAYS)

        print("Start:", start)
        print("End:", end)

        
        candles = mt5.copy_rates_range(
            SYMBOL,
            TIMEFRAME,
            start,
            end
        )

        if candles is None or len(candles) == 0:
            raise RuntimeError(
                f"No candles returned: {mt5.last_error()}"
            )

        
        df = pd.DataFrame(candles)

        # Convert timestamps to UTC
        df["time"] = pd.to_datetime(
            df["time"],
            unit="s",
            utc=True
        )

        
        df = (
            df.drop_duplicates(subset="time")
              .sort_values("time")
              .reset_index(drop=True)
        )

        
        if df.empty:
            raise RuntimeError("Downloaded data is empty.")

        if df["time"].isna().any():
            raise RuntimeError("Invalid timestamps found.")

        # Save historical data
        df.to_csv(OUTPUT_FILE, index=False)

        print("\nHistorical data downloaded successfully!")
        print("First candle:", df["time"].iloc[0])
        print("Last candle:", df["time"].iloc[-1])
        print("Total candles:", len(df))
        print("Saved to:", OUTPUT_FILE)

        return df

    finally:
        mt5.shutdown()


if __name__ == "__main__":
    get_market_data()

