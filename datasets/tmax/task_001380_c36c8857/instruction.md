You are a data engineer responsible for building an ETL pipeline to process time-series data from IoT sensors. The data is currently arriving in two different formats (CSV and JSONL) and contains dirty records that need to be cleaned and aggregated.

Your task is to write a Bash script or use standard Linux CLI tools (like `awk`, `jq`, `sort`, etc.) to process the raw logs, clean the data, and generate an hourly aggregated report.

Here are the details:

**Input Data:**
There are two files located in `/home/user/raw_data/`:
1. `/home/user/raw_data/stream1.csv`: A CSV file with the header `time,sensor,temp`.
2. `/home/user/raw_data/stream2.jsonl`: A JSON Lines file where each line is a JSON object with keys `ts` (timestamp), `id` (sensor ID), and `v` (temperature value).

**Requirements:**
1. **Combine & Normalize**: Parse both files into a common structure. The timestamps are in ISO 8601 format (e.g., `2023-11-01T08:15:30Z`).
2. **Clean**: 
   - Drop any records where the temperature value is missing (empty in CSV, or `null` in JSONL).
   - Deduplicate the dataset. If there are exact duplicate records (same timestamp, same sensor ID, same value) across or within the streams, keep only one.
3. **Time-Based Bucketing**: Truncate the timestamps to the start of the hour to create hourly buckets (e.g., `2023-11-01T08:15:30Z` becomes `2023-11-01T08:00:00Z`).
4. **Aggregate**: Calculate the average temperature for each sensor per hourly bucket.
5. **Output**: Save the results to `/home/user/etl_output/aggregated.csv`. 
   - The output must include a header row: `bucket,sensor,avg_temp`
   - `avg_temp` should be formatted to exactly two decimal places (e.g., `11.00`, `12.50`).
   - The output must be sorted chronologically by `bucket` (ascending), and then alphabetically by `sensor` ID.

Please execute the necessary commands to generate the output file. You do not need to submit the script, just ensure the final `/home/user/etl_output/aggregated.csv` file is created correctly.