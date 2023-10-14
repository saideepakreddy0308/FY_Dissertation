import os
import pandas as pd

# Set the working directory to your project directory
project_directory = 'C:/Users/saide/Documents/Final_Year_Dissertation/Economic_Indicators_Data'
os.chdir(project_directory)

# List of keywords to identify relevant Excel files (based on original filenames)
keywords = ['bci', 'cci', 'cli','ue_rate','short_term_interest_rates','long_term_interest_rates']

# Input and output directories
input_directory = 'data/raw_data'
output_directory = 'data/processed_data'

# Create the output directory if it doesn't exist
os.makedirs(output_directory, exist_ok=True)

# Get a list of Excel files in the input directory
excel_files = [file for file in os.listdir(input_directory) if file.lower().endswith(('.xls', '.xlsx'))]

# Iterate through Excel files and process the relevant ones
for file in excel_files:
    # Check if the original filename (without extension) contains any of the keywords
    filename_without_extension = os.path.splitext(file)[0]
    if any(keyword in filename_without_extension for keyword in keywords):
        # Read the Excel file
        data = pd.read_excel(os.path.join(input_directory, file))

        # Assuming 'TIME' is the 1st column (index 0) and 'VALUE' is the 3rd column (index 2)
        data.iloc[:, 0] = pd.to_datetime(data.iloc[:, 0], format='%Y-%m')
        data = data.iloc[:, [0, 2]]
        data = data.set_index('TIME').resample('D').interpolate()
        data.reset_index(inplace=True)
        data['TIME'] = data['TIME'].dt.strftime('%d-%m-%Y')

        # Define the transformed file name with the keyword
        transformed_file_name = f'{filename_without_extension}_processed_data.xlsx'

        # Save the transformed data to the output directory as Excel
        data.to_excel(os.path.join(output_directory, transformed_file_name), index=False)
