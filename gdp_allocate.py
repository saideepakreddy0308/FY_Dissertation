import pandas as pd
import numpy as np

# Create a sample daily data DataFrame for 2021
daily_data = pd.DataFrame({
    'date': pd.date_range(start='2021-01-01', end='2021-12-31', freq='D'),
})

# Create a sample quarterly GDP DataFrame for 2020 and 2021
quarter_gdp = pd.DataFrame({
    'quarter_start_date': ['2020-10-01', '2021-01-01', '2021-04-01', '2021-07-01', '2021-10-01'],
    'GDP': [20.8, 21.0, 21.2, 21.5, 21.8]
})

# Define a function for linear interpolation with 6 decimal points
def interpolate_gdp(start_gdp, end_gdp, total_days, day_number):
    interpolated_value = start_gdp + ((end_gdp - start_gdp) / total_days) * day_number
    return round(interpolated_value, 6)

# Initialize an empty list to store interpolated GDP values
gdp_interpolated = []

# Loop through each quarter to interpolate GDP
for i in range(len(quarter_gdp) - 1):
    start_date = pd.Timestamp(quarter_gdp.loc[i, 'quarter_start_date'])
    end_date = pd.Timestamp(quarter_gdp.loc[i + 1, 'quarter_start_date']) - pd.Timedelta(days=1)
    
    mask = (daily_data['date'] >= start_date) & (daily_data['date'] <= end_date)
    total_days = np.sum(mask)
    
    start_gdp = quarter_gdp.loc[i, 'GDP']
    end_gdp = quarter_gdp.loc[i + 1, 'GDP']
    
    for day_number in range(total_days):
        gdp_interpolated.append(interpolate_gdp(start_gdp, end_gdp, total_days, day_number))

# If there are still remaining days, fill them with the last known GDP value
remaining_days = len(daily_data) - len(gdp_interpolated)
gdp_interpolated += [round(quarter_gdp.loc[len(quarter_gdp) - 1, 'GDP'], 6)] * remaining_days

# Assign interpolated GDP values to the daily data DataFrame
daily_data['GDP'] = gdp_interpolated

# Show DataFrame
print(daily_data.head())
print(daily_data.tail())
