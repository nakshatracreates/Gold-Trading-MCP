# Gold Trading MCP

An AI-powered gold trading research and backtesting assistant built using Python, MetaTrader 5, MCP, and LangChain.

## Features

- Historical XAUUSD market data collection through MetaTrader 5.
- SMA 20/50 crossover strategy backtesting.
- Trade history and performance analysis.
- Candlestick and account balance visualizations.
- Risk calculation and position sizing tools.
- PostgreSQL-based trading journal.
- MCP server exposing trading tools.
- LangChain agent supporting continuous conversations.
- Backtest analysis for different time periods.

## Tech Stack

- Python
- MetaTrader 5
- Pandas
- Matplotlib
- mplfinance
- PostgreSQL
- SQLAlchemy
- FastMCP
- LangChain
- OpenAI API

## Project Workflow

1. Fetch historical gold market data from MT5.
2. Calculate SMA 20 and SMA 50.
3. Generate crossover signals and simulate trades.
4. Calculate backtest performance.
5. Generate charts and save trade history.
6. Expose trading functions through an MCP server.
7. Interact with the tools through a LangChain agent.

## Disclaimer

This project is for educational and research purposes only. The SMA 20/50 strategy is an experimental baseline and is not a recommendation to trade. Backtest results do not guarantee future performance.

## Setup

1. Clone the repository.
2. Create and activate a Python virtual environment.
3. Install dependencies using `pip install -r requirements.txt`.
4. Configure the required environment variables in a local `.env` file.
5. Ensure MetaTrader 5 is installed and connected.
6. Run the market data, backtesting, visualization, and agent scripts.

## Author

NakshatraPande
