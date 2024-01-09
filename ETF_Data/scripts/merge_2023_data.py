import pandas as pd
import glob

# Create an empty DataFrame to store the merged data
merged_data = pd.DataFrame()

# List all the files in the directory with a specific pattern (e.g., all CSV files)
files = glob.glob(r'ETF_Data\data\raw_data_2018_2023\*.csv')

# Loop through each file and append its data to the merged_data DataFrame
for file in files:  
    # Read the data from the current file
    current_data = pd.read_csv(file)
    
    # Calculate the percentage change and introduce a new column
    current_data['Percentage Change'] = current_data['Close'].pct_change() * 100
    
    # Append the current data to the merged_data DataFrame
    merged_data = merged_data.append(current_data, ignore_index=True)

# Save the merged data to a new CSV file or perform further analysis
merged_data.to_csv(r'ETF_Data\data\merged_data_2018_2023_with_percentage_change.csv', index=False)

# Create a pivot table
pivot_table = merged_data.pivot_table(index='Date', columns='Ticker', values='Percentage Change')

# Save the pivot table to a new CSV file
pivot_table.to_csv(r'ETF_Data\data\pivot_table_2018_2023.csv')
