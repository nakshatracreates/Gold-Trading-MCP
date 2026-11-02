from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Gold Trading Tools")
from trading_tools import (
    calculate_risk_amount,
    calculate_position_size,
    get_gold_data,
    get_backtest_results,
    run_sma_backtest,
)
from journal import(save_trade,Trade)




@mcp.tool()
def risk_amount(balance: float, risk_percentage: int) -> float:
    """Calculate the money at risk for a trade."""
    return calculate_risk_amount(balance, risk_percentage)


@mcp.tool()
def position_size(
    risk_amount: float,
    stop_loss_distance: float,
    value_per_dollar_per_lot: float,
) -> float:
    """Calculate position size in lots for a gold trade."""
    return calculate_position_size(
        risk_amount,
        stop_loss_distance,
        value_per_dollar_per_lot,
    )

@mcp.tool()
def save_trade_record(
    symbol: str,
    direction: str,
    entry_price: float,
    stop_loss: float,
    lot_size: float,
) -> str:
    """Save a trade record to the PostgreSQL trading journal."""
    trade = Trade(
        symbol=symbol,
        direction=direction,
        entry_price=entry_price,
        stop_loss=stop_loss,
        lot_size=lot_size,
    )

    saved_trade = save_trade(trade)
    return f"Trade saved successfully with ID {saved_trade.id}."

@mcp.tool()
def analyze_backtest(days:int) -> dict:
    """Analyze the latest SMA 20/50 backtest performance."""
    return run_sma_backtest(days=days)

if __name__ == "__main__":
    mcp.run(transport="stdio")

