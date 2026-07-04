You are a data analyst working with an IoT temperature sensor that sometimes drops network packets, leading to missing data. 

You have been given a CSV file located at `/home/user/sensor_data.csv` containing two columns: `timestamp` (in epoch seconds) and `value` (temperature in Celsius). The sensor is supposed to report every 60 seconds starting from epoch `1600000000` up to `1600001800`, but several readings are missing.

Your task is to write a bash-only data processing pipeline (using tools like `awk`, `sed`, `grep`, `bash` built-ins, etc. - do not use Python or other high-level languages) that performs the following steps:

1. **Resampling and Gap-filling**: Create a continuous time series from `1600000000` to `1600001800` inclusive, at strictly 60-second intervals. Where a timestamp is missing, forward-fill the value (use the last available prior reading). The first timestamp (`1600000000`) is guaranteed to be present.
2. **Rolling Statistics**: Compute a 3-period (i.e., 3-minute) rolling average of the gap-filled temperature values. For the first two minutes, compute the average using only the available history (e.g., period 1 is just the first value, period 2 is the average of the first two values).
3. **Downsampling / Stratification**: Extract only the rows where the timestamp corresponds to every 5 minutes (i.e., timestamp modulo 300 equals 0).
4. **Formatting**: Output the final downsampled data to `/home/user/processed_sensor.csv`. The output must include a header `timestamp,rolling_avg`. The `rolling_avg` should be rounded to exactly two decimal places (e.g., `14.67`).

**Constraints**:
- Use only standard Linux command-line tools.
- Output file strictly formatted as requested.