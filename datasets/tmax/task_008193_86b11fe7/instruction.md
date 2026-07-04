You are a data scientist working with a raw, corrupted dataset of server room temperatures. The data pipeline has dumped a pipe-separated file at `/home/user/dirty_temperatures.txt`.

Your goal is to clean, impute, and normalize this dataset using Bash shell utilities (like `awk`, `sed`, `grep`, or pure bash). Write a script or a pipeline that produces a cleaned CSV file at `/home/user/clean_normalized.csv`.

Here are the strict data processing rules you must implement:

1. **Regex Filter**: The first column is a timestamp. Keep only rows where the timestamp strictly matches the ISO8601 format: `YYYY-MM-DDThh:mm:ssZ` (e.g., `2023-10-01T10:00:00Z`). Discard rows with malformed timestamps.
2. **Anomaly Detection**: The second column is temperature in Celsius. Any temperature strictly greater than `60.0` or strictly less than `-40.0` is a sensor anomaly. Completely discard rows containing anomalous temperatures.
3. **Imputation (Forward Fill)**: Sometimes the temperature column is missing (empty), but the timestamp is valid. Replace the missing temperature with the *last valid, non-anomalous temperature* observed in the data. (You may assume the first valid row will always have a valid temperature).
4. **Normalization**: After applying rules 1-3, apply Min-Max scaling to the temperatures. Map the minimum cleaned temperature to `0.0000` and the maximum to `1.0000`. Formula: `(value - min) / (max - min)`.
5. **Output Format**: Write the results to `/home/user/clean_normalized.csv`. The file must be comma-separated, have a header `timestamp,normalized_temp`, and the normalized temperatures must be formatted to exactly 4 decimal places (e.g., `0.2500`).

Ignore the header `timestamp|temperature_celsius` in the input file during processing, but make sure your output file has the exact header specified above.