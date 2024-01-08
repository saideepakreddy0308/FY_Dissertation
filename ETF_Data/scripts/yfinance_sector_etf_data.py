import os
import yfinance as yf
import pandas as pd

# Define ETF tickers grouped by sector
etf_by_sector = {
    "Commodities": ["GLD", "SLV", "PPLT", "PALL", "JJC", "JJU", "UNG"],
    "Agriculture": ["CORN", "SOYB", "WEAT", "BAL", "JO"],
    "Crude Oil": ["USO", "BNO"],
    "Technology": ["QQQ", "SMH", "HACK", "SKYY", "BOTZ"],
    "Finance": ["XLF", "KBE", "KRE", "KIE"],
    "Healthcare": ["XLV", "XBI", "PJP", "IHI"],
    "Market Benchmark": ["SPY"]
}

# Define date range (for this example, past 7 years, as two years in the data are helpful for feature engineering)
# start_date = "2016-01-01"
start_date = "2023-01-01"
end_date = "2023-12-31"
# end_date = "2023-07-31"

# Create a directory to store the ETF data if it doesn't already exist
main_directory = "ETF_Data"
sub_directory = "data"
data_directory = "raw_etf_data"

directory_to_create = os.path.join(main_directory, sub_directory, data_directory)

if not os.path.exists(directory_to_create):
    os.makedirs(directory_to_create)

def download_data():
    for sector, etf_list in etf_by_sector.items():
        for ticker in etf_list:
            # Fetch data from Yahoo Finance
            data = yf.download(ticker, start=start_date, end=end_date)
            
            # Check for missing values in the data
            if data.isnull().values.any():
                print(f"Warning: Missing values found in data for {ticker}")
            
            # Add 'Sector' and 'Ticker' columns
            data['Sector'] = sector
            data['Ticker'] = ticker

            # Save the data to a CSV file in the desired directory
            csv_filename = os.path.join(main_directory, sub_directory, data_directory, f"{sector}_{ticker}_{start_date}_to_{end_date}.csv")
            data.to_csv(csv_filename)
            print(f"Data for {ticker} in sector {sector} has been saved to {csv_filename}.")

# Run the download
download_data()
