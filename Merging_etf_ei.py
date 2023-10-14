import pandas as pd

# Specify the paths to the two input Excel files
input_file1 = 'Training_Data/merged_etf_data.xlsx'
input_file2 = 'Training_Data/merged_ei_data.xlsx'

# Read the data from the two files
dataset1 = pd.read_excel(input_file1)
dataset2 = pd.read_excel(input_file2)

# Convert 'Date' column to datetime data type in both datasets
dataset1['Date'] = pd.to_datetime(dataset1['Date'])
dataset2['Date'] = pd.to_datetime(dataset2['Date'])

# Merge the two datasets on the 'Date' column
merged_data = pd.merge(dataset1, dataset2, on='Date', how='outer')

# Specify the output file path
output_file = 'Training_Data/etf_ei_merged_data.xlsx'

# Write the merged data to an Excel file
merged_data.to_excel(output_file, index=False)

print(f'Merged data saved to {output_file}')
