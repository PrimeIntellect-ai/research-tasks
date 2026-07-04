You are acting as an AI assistant for a localization engineer. The engineer has received a raw telemetry log from various regional servers tracking instances where users encountered untranslated strings in the app UI. 

The raw data is stored at `/home/user/loc_telemetry.csv`. Because the logs were aggregated from an older Windows-based logging system, the file is encoded in `UTF-16LE`.

Your task is to write and execute a Python script that processes this file to help the engineer understand the frequency of a specific missing translation over time.

Please perform the following data processing steps:
1. Read the `/home/user/loc_telemetry.csv` file using the correct character encoding.
2. Filter the dataset to include only rows where the `missing_key` column is exactly `error.network_timeout`.
3. Set up the `date` column as a time-series index.
4. Resample the data to a daily frequency ('D'). Since the logs only record days where an error occurred, you must gap-fill any missing days in the date range (from the earliest to the latest date in the filtered dataset) with a `count` of `0`.
5. Calculate a 3-day rolling sum of the daily error counts. (Use a window size of 3 days. The sum for a given day should include that day and the two preceding days. Use `min_periods=1` so the first two days aren't left as NaN).
6. Save the final processed data to `/home/user/loc_rolling_report.csv`.

**Output Specifications for `/home/user/loc_rolling_report.csv`:**
* The file must be strictly encoded in `UTF-8`.
* It must contain exactly two columns: `date` and `rolling_count`.
* The `date` column must be formatted as `YYYY-MM-DD`.
* The `rolling_count` should be expressed as integers (e.g., `5`, not `5.0`).
* Include a header row.

Write the Python code, save it, and execute it to produce the output file.