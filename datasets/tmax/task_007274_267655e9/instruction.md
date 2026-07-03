You are tasked with normalizing and analyzing an irregular event log for a configuration management system. A microservice architecture has its configuration updates logged asynchronously. We need to analyze the `max_connections` configuration metric for the `web` service to understand sustained capacity limits.

The raw log file is located at `/home/user/config_updates.jsonl` (JSON Lines format). It contains timestamps and configuration parameters for various services.

Write a Python script (save it wherever you like, but execute it to produce the final output) that performs the following data processing steps:

1. **Filter**: Extract only the events where `"service"` is `"web"`.
2. **Resample & Impute**: 
   - Align the irregular timestamps to an exact hourly grid (e.g., `08:00:00`, `09:00:00`) spanning from the start of the first hour in the filtered dataset to the start of the last hour required to capture the final event.
   - For each hourly boundary, determine the active `max_connections` limit. To do this, use **forward-filling** (the configuration limit stays the same until a new event updates it). 
   - If the earliest event happens after the first hourly boundary (e.g., event at `08:12`, boundary at `08:00`), **back-fill** that initial boundary with the value from the first subsequent event so no hourly slots are null.
3. **Rolling Aggregation**:
   - Compute a 3-hour rolling average (`rolling_avg_3h`) of the `max_connections` limit.
   - This rolling window should include the current hour and the previous 2 hours.
   - Require exactly 3 periods (hours) of data to compute this average. Leave as `NaN` or drop rows where the full 3-hour window is not available.
4. **Format & Output**:
   - Save the processed data to `/home/user/web_hourly_metrics.csv`.
   - The CSV must contain exactly three columns: `timestamp` (format `YYYY-MM-DD HH:00:00`), `max_connections` (integer), and `rolling_avg_3h` (float, rounded to exactly 2 decimal places).
   - Only include rows in the final CSV where `rolling_avg_3h` has a valid computed value (drop rows with missing rolling averages).

Ensure your script processes the file completely and generates the exact output CSV at `/home/user/web_hourly_metrics.csv`. You may install and use standard data processing libraries like `pandas` if they help.