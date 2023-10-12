import os
import pandas as pd
import numpy as np

# Define the input and output directories
input_dir = "ETF_Data/data/processed_etf_data"
output_dir = "ETF_Data/data/transformed_etf_data"

# Create the output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Get a list of files in the input directory
input_files = os.listdir(input_dir)

# Loop through each input file
for input_file in input_files:
    # Create the full path for the input and output files
    input_path = os.path.join(input_dir, input_file)
    output_file = "transformed_" + input_file
    output_path = os.path.join(output_dir, output_file)

    # Load your original data
    data = pd.read_csv(input_path)

    # Extract Sector and Ticker values from the first row (assuming they are in the first row)
    first_row = data.iloc[0]
    sector = first_row.get("Sector", None)
    ticker = first_row.get("Ticker", None)

    # Set 'Date' column as the index
    data['Date'] = pd.to_datetime(data['Date'])
    data.set_index('Date', inplace=True)

    # Create a new date range with daily frequency from 2017-12-20 to 2022-12-31
    date_range = pd.date_range(start='2016-01-01', end='2022-12-31', freq='D')

    # Create a DataFrame with missing dates
    missing_data = pd.DataFrame(index=date_range)

    # Merge the missing_data with the original data using left join
    combined_data = missing_data.join(data)

    # Interpolate only for the missing values in combined_data
    combined_data = combined_data.interpolate(method='linear')

    # Set the same Sector and Ticker for all rows
    combined_data['Sector'] = sector
    combined_data['Ticker'] = ticker

    # Calculate the columns as needed
    combined_data['log_return'] = np.log(combined_data['Close'] / combined_data['Close'].shift(1))
    combined_data['daily_return'] = combined_data['Close'] / combined_data['Close'].shift(1) - 1
    combined_data['volatility'] = combined_data['daily_return'].rolling(window=20).std()
    combined_data['momentum'] = combined_data['Close'] / combined_data['Close'].shift(20) - 1
    combined_data['MA_50'] = combined_data['Close'].rolling(window=50).mean()
    combined_data['MA_100'] = combined_data['Close'].rolling(window=100).mean()
    combined_data['MA_200'] = combined_data['Close'].rolling(window=200).mean()
    combined_data['Direction'] = combined_data['daily_return'].apply(lambda x: 1 if x > 0 else 0)

    # Reset the index to have 'Date' as a regular column
    combined_data.reset_index(inplace=True)

    # Rename the first column to 'Date'
    combined_data.rename(columns={combined_data.columns[0]: 'Date'}, inplace=True)

    # Save the transformed data to the output directory
    combined_data.to_csv(output_path, index=False)