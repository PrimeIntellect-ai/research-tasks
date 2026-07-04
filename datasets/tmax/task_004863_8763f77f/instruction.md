You are a data engineer responsible for processing data from two IoT temperature sensors in a smart home environment. The data is arriving in different formats, contains duplicates, and has missing records due to network drops.

Your task is to build a small ETL pipeline that unifies, cleans, and enriches this data, saving the final output to `/home/user/processed_data.csv`.

Here is the setup:
- **Sensor A** data is located at `/home/user/sensor_a.csv` with columns `ts_sec,temp`.
- **Sensor B** data is located at `/home/user/sensor_b.json` as an array of objects: `[{"time": <ts>, "t": <temp>}, ...]`.

You must perform the following steps to produce the final dataset:

1. **Unify and Deduplicate**: 
   Combine the records from both sensors. Sensor A's ID should be `A`, and Sensor B's ID should be `B`. 
   If there are duplicate records for the same sensor and timestamp, keep only the record with the **maximum** temperature.

2. **Resample and Gap-Fill**: 
   The target time range is from `1672531200` to `1672531500` (inclusive) at exactly **60-second intervals** (i.e., 1672531200, 1672531260, 1672531320, etc.). 
   For each sensor, if a timestamp in this grid is missing, use **forward-fill** (carry over the last observed temperature for that sensor). You may assume the first timestamp (`1672531200`) is present for both sensors.

3. **Compute Rolling Statistics**: 
   Calculate a **3-period Simple Moving Average (SMA)** of the temperature for each sensor based on the resampled 60-second grid. 
   - The SMA for a given timestamp should be the average of the temperature at that timestamp and the two preceding timestamps.
   - For the first two intervals of each sensor, the SMA cannot be computed. Leave the field completely empty.

4. **Output Format**:
   Save the final data to `/home/user/processed_data.csv`.
   - The file must have the header: `timestamp,sensor_id,temperature,sma_3`
   - Sort the rows chronologically by `timestamp` ascending. If timestamps are equal, sort alphabetically by `sensor_id` ascending.
   - Format `temperature` and `sma_3` to exactly **2 decimal places** (e.g., `20.00`, `21.50`, `18.33`).

You can use any language or standard CLI tools available in a standard Linux environment (e.g., Python, Bash, awk, jq).