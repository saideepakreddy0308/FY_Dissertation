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

# Define date range (for this example, past 6 years, as first year in the data just for feature engineering)
start_date = "2017-01-01"
end_date = "2022-12-31"

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

            # Save the data to an Excel file in the desired directory
            excel_filename = os.path.join(main_directory, sub_directory, data_directory, f"{sector}_{ticker}_{start_date}_to_{end_date}.xlsx")
            data.to_excel(excel_filename, index=False)
            print(f"Data for {ticker} in sector {sector} has been saved to {excel_filename}.")

# Run the download
download_data()