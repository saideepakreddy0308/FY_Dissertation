import os
import pandas as pd

# Set the working directory to your project directory
project_directory = ''
os.chdir(project_directory)

# List of keywords to identify relevant CSV files (based on original filenames)
keywords = ['bci', 'cci', 'cli', 'ue_rate', 'long_term_interest_rates']

# Input and output directories
input_directory = 'data/raw_data'
output_directory = 'data/processed_data'

# Create the output directory if it doesn't exist
os.makedirs(output_directory, exist_ok=True)

# Get a list of CSV files in the input directory
csv_files = [file for file in os.listdir(input_directory) if file.lower().endswith('.csv')]

# Iterate through CSV files and process the relevant ones
for file in csv_files:
    # Check if the original filename (without extension) contains any of the keywords
    filename_without_extension = os.path.splitext(file)[0]
    if filename_without_extension in keywords:
        # Read the CSV file
        data = pd.read_csv(os.path.join(input_directory, file), sep='\t')
        
        # Perform linear interpolation and change the date format
        data.iloc[:, 5] = pd.to_datetime(data.iloc[:, 5], format='%Y-%m')
        data = data.iloc[:, [5, 6]]  # Keep only the 6th and 7th columns
        data = data.set_index(data.columns[0]).resample('D').interpolate()
        data.reset_index(inplace=True)
        data.iloc[:, 0] = data.iloc[:, 0].dt.strftime('%d-%m-%Y')
        
        # Define the transformed file name with the keyword
        transformed_file_name = f'{filename_without_extension}_processed_data.csv'
        
        # Save the transformed data to the output directory as CSV
        data.to_csv(os.path.join(output_directory, transformed_file_name), index=False)
