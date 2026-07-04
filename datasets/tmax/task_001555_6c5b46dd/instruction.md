You are a data scientist tasked with cleaning and summarizing a partitioned dataset of user telemetry events. 

The raw data is stored in partitioned CSV files located in the directory `/home/user/telemetry_data/`. 

Write a Python script at `/home/user/clean_data.py` that performs the following pipeline:
1. **Data Loading:** Read and combine all CSV files found in `/home/user/telemetry_data/`.
2. **Data Cleaning:** 
   - Remove any rows where the `latency_ms` is strictly less than 0 (these are logging errors).
   - Remove any rows where the `event_type` is missing (null) or is an empty string.
3. **Imputation:** Fill any missing (null) values in the `payload_size` column with the global median of the valid `payload_size` values.
4. **Feature Engineering:** Create a new column named `is_high_latency` which equals `1` if `latency_ms` is strictly greater than `1000`, and `0` otherwise.
5. **Aggregation:** Group the cleaned data by `user_id` and compute the following metrics for each user:
   - `event_count`: The total number of valid events.
   - `avg_latency`: The mean of `latency_ms` (as a float).
   - `high_latency_count`: The sum of `is_high_latency`.
6. **Output:** Save the aggregated data to a CSV file at `/home/user/cleaned_summary.csv`. The output file must contain exactly the columns `user_id`, `event_count`, `avg_latency`, and `high_latency_count` (in that order), and must be sorted by `user_id` in ascending order. Do not include the dataframe index in the CSV.

Run your script to produce the final `/home/user/cleaned_summary.csv` file.