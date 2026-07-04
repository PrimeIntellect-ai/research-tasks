You are an ETL data engineer. Due to an upstream retry bug, our recent metrics extraction job produced duplicate records. Your task is to clean, reshape, and calculate rolling statistics on the data using Linux command-line tools.

The raw data is located at `/home/user/raw_data.csv` with the following header:
`run_id,timestamp,sensor1,sensor2`

You must write a processing pipeline (using bash, awk, sort, etc., or a small script) that performs the following steps:

1. **Deduplicate (DAG / Grouping):** Because of the retry bug, there are multiple rows for the same `timestamp`. Group the records by `timestamp` and strictly keep only the row with the maximum `run_id`.
2. **Reshape (Wide to Long):** Convert the deduplicated wide data into a long format. Each `timestamp` will now have multiple rows, one for each sensor. The resulting columns should be `timestamp,sensor_name,value`.
3. **Rolling Statistics Computation:** For each `sensor_name` (ordered chronologically by `timestamp`), calculate a simple moving average (SMA) of the `value` over a rolling window of 3 periods (the current row and the up to 2 preceding rows for that same sensor).
4. **Output formatting:** Save the final result to `/home/user/clean_data.csv`.
   - The file must have the header: `timestamp,sensor_name,value,rolling_avg`
   - The data must be sorted alphabetically by `sensor_name` (ascending), and then by `timestamp` (ascending).
   - The `rolling_avg` must be rounded to exactly two decimal places (e.g., `10.50`, `11.33`).
   - Fields should be comma-separated.

Create the file `/home/user/clean_data.csv` matching these exact specifications.