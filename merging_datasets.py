import pandas as pd
import os

# Create a list to hold DataFrames
dfs = []

# Load each file and add an 'ETF' column
for filename in os.listdir("etf_data"):
    if filename.startswith("preprocessed_"):
        ticker = filename.split('_')[1]
        df = pd.read_csv(f"etf_data/{filename}")
        df['ETF'] = ticker
        dfs.append(df)

# Concatenate all DataFrames into a single DataFrame
merged_df = pd.concat(dfs, ignore_index=True)

# Save this merged DataFrame for later use
merged_df.to_csv("etf_data/preprocessed_merged_data.csv", index=False)
