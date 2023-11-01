import pandas as pd
import numpy as np
import os

# Function to Load Data
def load_data(sector, ticker, start_date, end_date):
    file_path = f"ETF_Data/data/raw_etf_data/{sector}_{ticker}_{start_date}_to_{end_date}.csv"
    print(f"Trying to load {file_path}")
    try:
        df = pd.read_csv(file_path)
        return df
    except FileNotFoundError as e:
        print(f"File not found: {file_path}")
        return None

# Main code execution
if __name__ == "__main__":
    print(f"Current working directory: {os.getcwd()}")  # Print the current working directory
    
    start_date = "2016-01-01"
    end_date = "2023-07-31"
    
    sectors_tickers = {
        "Commodities": ["GLD", "SLV", "PPLT", "PALL", "JJC", "JJU", "UNG"],
        "Agriculture": ["CORN", "SOYB", "WEAT", "BAL", "JO"],
        "Crude Oil": ["USO", "BNO"],
        "Technology": ["QQQ", "SMH", "HACK","SKYY","BOTZ"],
        "Finance": ["XLF","KBE", "KRE", "KIE"],
        "Healthcare": ["XLV", "XBI", "PJP","IHI"],
        "Market Benchmark": ["SPY"]
        # Add more sectors and their tickers here
    }
    
    for sector, tickers in sectors_tickers.items():
        print(f"Processing data for sector: {sector}")
        
        for ticker in tickers:
            print(f"  Processing data for ticker: {ticker}...")
            
            # Load Data
            df = load_data(sector, ticker, start_date, end_date)
            
            # Data Cleaning
            
            # Handling Missing Values
            if df.isnull().any().any():
                df.fillna(method='ffill', inplace=True)
            
            # Handling Outliers
            z_scores = (df - df.mean()) / df.std()
            outliers = (z_scores > 3).any(axis=1)
            df = df[~outliers]
            
            # Data Transformation
            
            # Numerical Transformations: Log Returns
            df['log_return'] = np.log(df['Close'] / df['Close'].shift(1))
            
            # Daily Returns
            df['daily_return'] = (df['Close'] / df['Close'].shift(1)) - 1
            
            # Volatility
            df['volatility'] = df['daily_return'].rolling(window=21).std() * np.sqrt(252)
            
            # Momentum
            df['momentum'] = df['Close'] / df['Close'].rolling(window=90).mean() - 1
            
            # Categorical Data: Direction
            df['Direction'] = np.where(df['log_return'] > 0, 1, 0)
            
            # Date-Time Formatting
            df['Date'] = pd.to_datetime(df['Date'])
            
            # Data Resampling: Weekly Average
            weekly_data = df.resample('W', on='Date').mean()
            
            # Feature Engineering: Moving Averages
            df['MA_50'] = df['Close'].rolling(window=50).mean()
            df['MA_100'] = df['Close'].rolling(window=100).mean()
            df['MA_200'] = df['Close'].rolling(window=200).mean()
            
            # Remove first year data to start from "2017-12-20"
            # df = df[df['Date'] >= "2017-12-20"]
            
            # Saving pre-processed DataFrame for further steps
            save_path = f"ETF_Data/data/processed_etf_data/preprocessed_{sector}_{ticker}_2016-01-01_to_{end_date}.csv"
            df.to_csv(save_path, index=False)
            print(f"  Saved processed data to {save_path}")