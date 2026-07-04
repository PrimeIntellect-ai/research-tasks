As a data scientist, I need you to clean up a messy telemetry dataset using Rust. 

The raw data is located at `/home/user/telemetry_raw.csv`. It has two columns: `timestamp` (integer epoch seconds) and `sensor_data` (a messy string containing the sensor reading).

Here is a sample of the data:
```csv
timestamp,sensor_data
1700000100,"temp_val=10.0"
1700000101,"val=12.0C"
1700000103,"[WARN] val=12.0"
1700000104,"val=15.0"
```

Please write and execute a Rust program (create a Cargo project at `/home/user/processor`) that does the following in a single pipeline:

1. **Regex Extraction**: Extract the floating-point number immediately following `val=` in the `sensor_data` column.
2. **Resampling and Gap-Filling**: The timestamps should be contiguous, incrementing by exactly 1 second from the earliest timestamp to the latest timestamp in the file. If a timestamp is missing (e.g., `1700000102`), forward-fill the value using the most recent successfully parsed sensor value.
3. **Rolling Statistics**: Compute a 3-second rolling average of the resampled data. The window should be right-aligned (the average at time $T$ includes $T$, $T-1$, and $T-2$). For the first two rows where 3 values aren't available, compute the average of the available values.
4. **Output**: Write the final processed data to `/home/user/cleaned_telemetry.csv` with two columns: `timestamp` and `rolling_avg`. The `rolling_avg` should be formatted to exactly two decimal places.

Ensure you run your Rust program so the output file is generated.