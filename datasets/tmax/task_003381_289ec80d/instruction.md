You are tasked with cleaning and aggregating a dataset of sensor readings that was corrupted during a failed ETL pipeline retry. The retry caused duplicate records to be written across multiple CSV shards.

The raw data is located in `/home/user/sensor_data/` and consists of multiple CSV files (`shard_1.csv`, `shard_2.csv`, etc.). 
Each CSV has the following columns:
- `event_time`: The time the reading was taken (format: `YYYY-MM-DD HH:MM:SS`)
- `sensor_id`: The ID of the sensor (e.g., `S1`, `S2`)
- `temperature`: The recorded temperature (float)
- `ingested_at`: The UNIX timestamp when the ETL job processed the record

Write a Python script at `/home/user/process_sensors.py` to perform the following operations:

1. **Parallel Extraction**: Use Python's `multiprocessing` or `concurrent.futures` module to read all CSV files in the `/home/user/sensor_data/` directory in parallel.
2. **Hash-based Deduplication**: The ETL retry created duplicates. Generate an MD5 hash of the string concatenation of `event_time`, `sensor_id`, and `temperature` (formatted to 1 decimal place, e.g., "25.3") for each row. Use this hash as a unique identifier. If multiple records produce the same hash, keep ONLY the record with the highest (most recent) `ingested_at` value.
3. **Timestamp Alignment & Daily Aggregation**: Convert `event_time` to a calendar date (`YYYY-MM-DD`). For each `sensor_id` and calendar date, calculate the daily average temperature.
4. **Windowed Rolling Aggregation**: For each `sensor_id`, calculate a 3-day rolling average of the daily averages. The 3-day window for a given date includes that date and the 2 immediately preceding calendar days. Note: if a preceding calendar day has no data, the window will just average the days that *do* have data within that 3-day timeframe.
5. **Output**: Save the final rolling averages to `/home/user/rolling_averages.json`. The JSON structure must be a dictionary mapped by `sensor_id`, then by `YYYY-MM-DD` date strings, with the rolling average rounded to 2 decimal places.

Example Output Format:
```json
{
  "S1": {
    "2023-10-01": 22.50,
    "2023-10-02": 23.10,
    "2023-10-04": 22.85
  },
  "S2": { ... }
}
```

Run your script to generate the final `rolling_averages.json` file.