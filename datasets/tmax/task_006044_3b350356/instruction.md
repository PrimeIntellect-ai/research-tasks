You are an AI assistant helping an environmental researcher organize and analyze air quality datasets. 

The researcher has two files in their home directory:
1. `/home/user/sensor_data.csv`: Contains daily sensor readings from various sites. Columns are `site_id`, `date`, `temp`, `humidity`, and `pm25`.
2. `/home/user/site_info.json`: Contains metadata about the sites. It is a JSON list of dictionaries with keys `site_id`, `type`, and `elevation`.

Your task is to write and execute a Python script that performs the following steps:
1. Read and merge both datasets on `site_id`.
2. Aggregate the sensor readings to calculate the mean `temp`, mean `humidity`, and mean `pm25` for each `site_id`. Name these aggregated columns `mean_temp`, `mean_humidity`, and `mean_pm25`.
3. Create a new column called `type_encoded` by mapping the `type` string to an integer: `"Urban"` -> 1, `"Suburban"` -> 2, `"Rural"` -> 3.
4. Calculate the Pearson correlation matrix for the following five variables: `elevation`, `type_encoded`, `mean_temp`, `mean_humidity`, and `mean_pm25`.
5. Extract the upper triangle of the correlation matrix (excluding the diagonal).
6. Save these pairwise correlations to a JSON file at `/home/user/correlations.json`. 
   - The JSON should be a single dictionary.
   - The keys must be the two variable names separated by a double underscore `__`, in alphabetical order (e.g., `"elevation__mean_temp"`).
   - The values must be the Pearson correlation coefficient rounded to exactly 4 decimal places.

Ensure the final JSON file is properly formatted and contains exactly 10 key-value pairs representing all unique pairwise combinations of the 5 variables.