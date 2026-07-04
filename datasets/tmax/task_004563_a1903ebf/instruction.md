You are a data analyst tasked with processing a large dataset of sensor readings to identify anomalous devices. We need to compare the time-series behavior of several devices to a reference device ('Device_A').

You have been provided with a CSV file at `/home/user/sensor_data.csv` containing columns: `timestamp` (ISO 8601 format), `device_id`, and `value`. 

Your task is to write and execute a Python script (`/home/user/analyze.py`) that performs the following steps:

1. **Data Loading and Stratified Sampling**:
   - Load the CSV file.
   - Perform a stratified sample to retain exactly 50% of the data for each `device_id`. Use `pandas.DataFrame.sample(frac=0.5, random_state=42)` on the groups to ensure deterministic results.

2. **Time-Based Bucketing**:
   - Convert the `timestamp` column to datetime.
   - For each device, bucket the sampled data into 1-hour intervals (starting at the beginning of the hour, e.g., '2023-01-01 00:00:00') and calculate the mean `value` for that hour.
   - If any device has missing 1-hour intervals (after bucketing), fill them using forward fill (`ffill`), followed by backward fill (`bfill`). Ensure the time index is continuous covering the minimum to maximum hour of the whole dataset.

3. **Similarity Computation**:
   - Extract the hourly aggregated time series for the reference device: `Device_A`.
   - For every other device, compute the Euclidean distance between its hourly time series and `Device_A`'s time series.

4. **Logging and Monitoring**:
   - Your script must use Python's built-in `logging` module to write progress logs to `/home/user/pipeline.log`. At a minimum, log when sampling is complete, aggregation is complete, and distance computation is complete.

5. **Output**:
   - Save the computed distances to a JSON file at `/home/user/similarities.json`.
   - The format must be exactly:
     ```json
     {
       "distances": {
         "Device_B": 1.23,
         "Device_C": 4.56,
         "Device_D": 7.89,
         "Device_E": 0.12
       }
     }
     ```
   - Round the distance values to exactly 2 decimal places.

Ensure the final JSON file is created and properly formatted.