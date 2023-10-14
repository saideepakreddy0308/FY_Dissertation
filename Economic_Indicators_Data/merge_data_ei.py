import os
import pandas as pd

# Set the input and output directory paths
input_directory = 'Economic_Indicators_Data/data/transformed_data'
output_directory = 'Economic_Indicators_Data/data/merged_data'

# Create the output directory if it doesn't exist
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# Initialize an empty DataFrame to store the merged data
merged_data = None

# Get a list of all Excel files in the input directory
excel_files = [f for f in os.listdir(input_directory) if f.endswith('.xlsx')]

# Iterate through the Excel files and merge them
for file in excel_files:
    file_path = os.path.join(input_directory, file)
    df = pd.read_excel(file_path)

    # Rename the 'Value' column to match the file name (excluding the file extension)
    file_name = os.path.splitext(file)[0]
    df = df.rename(columns={'Value': file_name})

    # Merge data based on the 'Date' column
    if merged_data is None:
        merged_data = df
    else:
        merged_data = pd.merge(merged_data, df, on='TIME', how='outer')

# Create the output file path
output_file_path = os.path.join(output_directory, 'merged_data.xlsx')

# Write the merged data to an Excel file
merged_data.to_excel(output_file_path, index=False)

print(f'Merged data saved to {output_file_path}')
