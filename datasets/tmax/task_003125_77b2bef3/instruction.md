You are a data engineer tasked with building an ETL pipeline to process time-series sensor data. We have a CSV file located at `/home/user/sensor_data.csv` containing raw readings. 

Unfortunately, our in-house CSV parser, located at `/app/vendored/fast_csv_reader`, has a bug: it silently drops rows that contain embedded newlines within quoted fields. Many of our sensors have multi-line descriptions (e.g., `"Turbine\nAlpha"`), so we are losing critical data.

Your objectives are:

1. **Fix the Vendored Crate**: 
   Inspect and patch the Rust crate at `/app/vendored/fast_csv_reader`. It currently reads line-by-line using standard `BufRead::read_line` and discards lines that don't have the correct number of columns. You must modify it to correctly handle embedded newlines inside double quotes (`"`).

2. **Build the Processor**:
   Create a new Rust project at `/home/user/ts_processor`. It must use the fixed local `fast_csv_reader` crate as a dependency.

3. **Data Cleaning & Filtering**:
   Process `/home/user/sensor_data.csv` (Columns: `timestamp`, `sensor_name`, `reading`). Extract only the rows where the `sensor_name` is exactly `"Turbine\nAlpha"` (with the newline character). Sort these records in ascending order by `timestamp`.

4. **Feature Extraction & Anomaly Detection**:
   For the filtered and sorted data, compute a rolling window of the last 10 readings (including the current reading). 
   - If the window has fewer than 10 readings, it cannot be an anomaly.
   - For windows of size 10, calculate the moving average and the sample standard deviation.
   - Flag the current reading as an anomaly if its value deviates from the moving average by strictly more than `3.0 * standard_deviation`.

5. **Outputs**:
   - Write the exact Unix epoch `timestamp`s of all detected anomalies into a JSON array in `/home/user/anomalies.json` (e.g., `[1600000000, 1600000060]`).
   - Generate a templated Markdown report at `/home/user/report.md` exactly matching this format:
     ```markdown
     # Sensor Report: Turbine Alpha
     Total Anomalies Detected: <COUNT>
     First Anomaly Timestamp: <TIMESTAMP_OR_NONE>
     ```

**Note on Evaluation**: 
Your solution will be evaluated based on the F1 score of the anomalous timestamps you output in `/home/user/anomalies.json` compared to a hidden ground truth. You must achieve an F1 score of >= 0.95.