import os
import pandas as pd

# Define the input and output directories
input_dir = "ETF_Data/data/transformed_etf_data"
output_dir = "ETF_Data/data/merged_data"

# Create the output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Get a list of files in the input directory
input_files = os.listdir(input_dir)

# Initialize an empty DataFrame to store the merged data
merged_data = pd.DataFrame()

# Loop through each input file
for input_file in input_files:
    # Create the full path for the input file
    input_path = os.path.join(input_dir, input_file)

    # Load the transformed data
    data = pd.read_csv(input_path)

    # Filter data to remove dates before 01-01-2018
    data = data[data['Date'] >= '2018-01-01']

    # Append the filtered data to the merged_data DataFrame
    merged_data = merged_data.append(data, ignore_index=True)

# Create the output file path
output_file = "merged_etf_training_data.csv"
output_path = os.path.join(output_dir, output_file)

# Save the merged data to a single CSV file
merged_data.to_csv(output_path, index=False)
