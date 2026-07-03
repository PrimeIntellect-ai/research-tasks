You are a data engineer tasked with building an ETL pipeline to process raw telemetry data from a fleet of refrigerated delivery trucks. The raw data contains irregular timestamps, missing values, and requires several transformations before it can be used for downstream analytics and anomaly detection.

The input file is located at `/home/user/raw_telemetry.csv`. It contains the following columns:
- `timestamp`: ISO8601 formatted datetime.
- `truck_id`: String identifier (e.g., 'TRUCK_A').
- `temperature`: Float (can have missing values/NaN).
- `speed`: Float (can have missing values/NaN).

Please write and execute a Python script to perform the following ETL pipeline:

1. **Resampling and Gap-Filling**:
   - For each `truck_id`, resample the data to fixed **5-minute intervals**.
   - For `temperature`: Forward-fill missing values, but with a maximum limit of 2 consecutive fills (if a gap is larger, leave as NaN).
   - For `speed`: Use linear interpolation to fill missing values.

2. **Time-Based Bucketing and Aggregation**:
   - Aggregate the 5-minute resampled data into **1-hour tumbling windows** for each `truck_id`.
   - Calculate the following summary statistics per window:
     - `max_temp`: The maximum `temperature` in that hour.
     - `avg_speed`: The mean `speed` in that hour.
   - Ignore NaN values when computing the hour's max/mean.

3. **Rolling Aggregation**:
   - Create a new column `rolling_3h_max_temp` that computes the **3-hour rolling average** of the `max_temp` for each `truck_id` (including the current hour and the previous 2 hours). Ensure this does not leak data between different trucks.

4. **Stratified Sampling**:
   - Filter the hourly dataset to identify "High Risk" windows, defined as `max_temp > -10.0` OR `avg_speed > 75.0`.
   - Take a stratified sample to extract exactly **one highest-risk record per truck** (the record with the highest `max_temp` among the high-risk windows).

**Outputs Required**:
You must save your processed data to the following locations:
1. `/home/user/hourly_summary.csv`: The result of steps 1-3. Must contain columns `timestamp`, `truck_id`, `max_temp`, `avg_speed`, and `rolling_3h_max_temp`. The `timestamp` should represent the start of the 1-hour window.
2. `/home/user/high_risk_sample.csv`: The result of step 4. Must contain the same columns as `hourly_summary.csv`.

Ensure you install any necessary Python packages (like `pandas`) using `pip`.