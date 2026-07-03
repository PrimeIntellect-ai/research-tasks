You are a data analyst working with daily weather station data. You have received a messy CSV file located at `/home/user/weather_data.csv`. 

Your task is to write and execute a Python script (e.g., using `pandas`) to clean and process this file, saving the output to `/home/user/cleaned_weather.csv`.

The input CSV has the following columns: `station_id`, `station_name`, `date`, `temperature`.

Perform the following data processing steps in order:
1. **Deduplication:** Remove any exact duplicate rows. Keep the first occurrence.
2. **Unicode Normalization:** The `station_name` column contains identically-spelled cities but with mixed Unicode representations (e.g., precomposed characters vs. combining characters). Apply **NFKC** Unicode normalization to all strings in the `station_name` column, and strip any leading/trailing whitespace.
3. **Interpolation and Imputation:** The `temperature` column has missing values (empty strings). 
   - Group the data by `station_id`.
   - Ensure the data is sorted chronologically by `date` within each group.
   - For missing temperatures, perform **linear interpolation** based on the surrounding valid temperatures for that specific station.
   - If a temperature is missing at the very beginning or end of a station's time series (where linear interpolation can't work), fill it using **backward fill** (for leading missing values) or **forward fill** (for trailing missing values) within that station's group.
4. **Formatting and Output:** 
   - Sort the final dataset primarily by `station_id` (ascending) and secondarily by `date` (ascending).
   - Format the `temperature` column to exactly 1 decimal place (e.g., `5.0`, `7.5`).
   - Save the result to `/home/user/cleaned_weather.csv` with a comma delimiter and including the header.

Make sure you write the Python script and execute it so that `/home/user/cleaned_weather.csv` is generated successfully.