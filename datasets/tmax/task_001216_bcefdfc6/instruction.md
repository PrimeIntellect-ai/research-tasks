You are a data engineer responsible for building an ETL pipeline to process telemetry data from a network of industrial sensors. You need to handle multiple data formats, parse unstructured logs, resample time-series data, compute rolling aggregations, and orchestrate the workflow.

Your workspace is `/home/user/sensor_etl`. I have already placed the raw data in `/home/user/sensor_etl/data/`. 

The pipeline must perform the following tasks:

1. **Log Parsing (Regex & Multi-format)**:
   - Read `/home/user/sensor_etl/data/calibrations.log`.
   - Use regex to extract the timestamp, sensor ID, and calibration factor from log lines. 
   - A typical log line looks like: `[INFO] 2023-11-01T10:05:00Z - Sensor [S-01] calibrated. New multiplier: 1.05`
   - Ignore lines that do not match this calibration format (e.g., standard boot logs).

2. **Data Merging & Multi-format Handling**:
   - Read the metadata from `/home/user/sensor_etl/data/metadata.json`, which contains each sensor's baseline offset.
   - Read the raw irregular readings from `/home/user/sensor_etl/data/raw_readings.csv`.
   - For each reading, the true value is calculated as: `(raw_value * current_calibration_multiplier) - baseline_offset`. 
   - The `current_calibration_multiplier` is the most recent multiplier applied to that sensor *at or before* the reading's timestamp. If no calibration log exists prior to the reading, assume a default multiplier of `1.0`.

3. **Resampling & Gap-Filling**:
   - The time-series data must be resampled to strict **1-minute intervals** (e.g., `10:00:00`, `10:01:00`, `10:02:00`) for each sensor, covering the inclusive time range from `2023-11-01T10:00:00Z` to `2023-11-01T10:10:00Z`.
   - Use **forward-fill** for missing intervals. If the very first interval (`10:00:00`) has no preceding data, leave it blank (null/NaN).

4. **Windowed Aggregation**:
   - For the resampled 1-minute data, calculate a **3-minute rolling average** of the true value for each sensor. The window should include the current minute and the 2 preceding minutes (e.g., the average at `10:05:00` uses values from `10:03:00`, `10:04:00`, and `10:05:00`). 
   - Require at least 1 valid data point in the window to compute an average (if all are null, the average is null).

5. **Pipeline Orchestration**:
   - Write your processing logic in a language of your choice.
   - Create a `Makefile` at `/home/user/sensor_etl/Makefile` with a default `all` target that runs your pipeline. The pipeline should ultimately produce a single output CSV file at `/home/user/sensor_etl/output/final_metrics.csv`.

**Output Format Specification**:
The file `/home/user/sensor_etl/output/final_metrics.csv` must contain the following columns in exact order:
`timestamp,sensor_id,resampled_true_value,rolling_3min_avg`
- `timestamp`: ISO 8601 format (e.g., `2023-11-01T10:05:00Z`).
- `sensor_id`: The sensor identifier (e.g., `S-01`).
- `resampled_true_value`: Rounded to 2 decimal places (or empty if null).
- `rolling_3min_avg`: Rounded to 2 decimal places (or empty if null).
- Sort the final output chronologically by `timestamp`, then alphabetically by `sensor_id`.

Write the code, orchestrate it via the `Makefile`, and run `make` so the output file is generated.