import os
import schedule
import time
import yfinance as yf
import pandas as pd

# Define list of ETF tickers
etf_list = ["SPY", "QQQ", "EEM", "GLD", "SLV"]

# Define date range (for this example, past 5 years)
start_date = "2016-01-0"
end_date = "2021-01-01"

# Create directory to store data if it doesn't exist
if not os.path.exists("etf_data"):
    os.makedirs("etf_data")

def download_data():
    for ticker in etf_list:
        # Fetch data from Yahoo Finance
        data = yf.download(ticker, start=start_date, end=end_date)

        # Data integrity check for missing values
        if data.isnull().values.any():
            print(f"Warning: Missing values found in data for {ticker}")

        # Save data to CSV
        data.to_csv(f"etf_data/{ticker}_{start_date}_to_{end_date}.csv")

        print(f"Data for {ticker} saved.")

# Function to run the job every day
def job():
    print("Downloading ETF data...")
    download_data()
    print("Download complete.")

# Schedule the job to run once every day
schedule.every().day.at("09:00").do(job)

# Keep the script running
while True:
    schedule.run_pending()
    time.sleep(1)
