import os
import yfinance as yf
import pandas as pd

# Define list of ETF tickers
etf_list = ["SPY", "QQQ", "EEM", "GLD", "SLV"]  # You can add more tickers here

# Define date range (for this example, past 5 years)
start_date = "2016-01-01"
end_date = "2020-12-31"

# Create a directory to store the ETF data if it doesn't already exist
if not os.path.exists("etf_data"):
    os.makedirs("etf_data")

def download_data():
    for ticker in etf_list:
        # Fetch data from Yahoo Finance
        data = yf.download(ticker, start=start_date, end=end_date)

        # Check for missing values in the data
        if data.isnull().values.any():
            print(f"Warning: Missing values found in data for {ticker}")

        # Save the data to a CSV file
        data.to_csv(f"etf_data/{ticker}_{start_date}_to_{end_date}.csv")

        print(f"Data for {ticker} has been saved.")

# Run the download
download_data()
