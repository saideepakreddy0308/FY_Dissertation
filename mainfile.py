import yfinance as yf

# For Equity-based ETF (e.g., SPY)
equity_etf = yf.download('SPY', start='2010-01-01', end='2021-09-01')

# Displaying the first few rows
print(equity_etf.head())

# For Daily Timeframe
# daily_data = yf.download('SPY', start='2010-01-01', end='2021-09-01', interval='1d')

# For Monthly Timeframe
# monthly_data = yf.download('SPY', start='2010-01-01', end='2021-09-01', interval='1mo')

# For Quarterly Timeframe
# quarterly_data = yf.download('SPY', start='2010-01-01', end='2021-09-01', interval='3mo')
