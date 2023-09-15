import pandas as pd
import numpy as np

# Function to Load Data
def load_data(ticker, start_date, end_date):
    file_path = f"etf_data/{ticker}_{start_date}_to_{end_date}.csv"
    df = pd.read_csv(file_path)
    return df

# Main code execution
if __name__ == "__main__":
    ticker = "QQQ"  # Example Ticker
    start_date = "2016-01-01"
    end_date = "2020-12-31"
    
    # Step 1.1: Load Data
    df = load_data(ticker, start_date, end_date)
    
    # Step 1.2: Data Cleaning
    
    # Handling Missing Values
    if df.isnull().any().any():
        df.fillna(method='ffill', inplace=True)
    
    # Handling Outliers
    z_scores = (df - df.mean()) / df.std()
    outliers = (z_scores > 3).any(axis=1)
    df = df[~outliers]
    
    # Step 1.3: Data Transformation
    
    # Numerical Transformations: Log Returns
    df['log_return'] = np.log(df['Close'] / df['Close'].shift(1))
    
    # Categorical Data: Direction
    df['Direction'] = np.where(df['log_return'] > 0, 1, 0)
    
    # Date-Time Formatting
    df['Date'] = pd.to_datetime(df['Date'])
    
    # Data Resampling: Weekly Average
    weekly_data = df.resample('W', on='Date').mean()
    
    # Feature Engineering: Moving Average
    df['MA_50'] = df['Close'].rolling(window=50).mean()
    
    # Saving pre-processed DataFrame for further steps
    df.to_csv(f"etf_data/preprocessed_{ticker}_{start_date}_to_{end_date}.csv", index=False)
