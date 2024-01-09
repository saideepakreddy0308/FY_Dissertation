import pandas as pd
import glob

# Create an empty DataFrame to store the merged data
merged_data = pd.DataFrame()

# List of tickers to be excluded
excluded_tickers = ["BAL", "JO", "JJC", "JJU"]

# List all the files in the directory with a specific pattern (e.g., all CSV files)
files = glob.glob(r'ETF_Data\data\raw_data_2018_2023\*.csv')

# Loop through each file and append its data to the merged_data DataFrame
for file in files:
    # Read the data from the current file
    current_data = pd.read_csv(file)
    
    # Exclude records with specified tickers
    current_data = current_data[~current_data['Ticker'].isin(excluded_tickers)]
    
    # Append the filtered data to the merged_data DataFrame
    merged_data = merged_data.append(current_data, ignore_index=True)

# Save the merged and filtered data to a new CSV file or perform further analysis
merged_data.to_csv(r'ETF_Data\data\merged_data_2018_2023_filtered.csv', index=False)
