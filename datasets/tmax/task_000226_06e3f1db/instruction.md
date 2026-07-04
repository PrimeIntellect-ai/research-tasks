You are a data engineer for an industrial IoT company building a high-performance ETL pipeline. We are migrating our quality control anomaly detection system to Rust.

You have been given two inputs:
1. A large historical dataset of sensor readings located at `/home/user/data/readings.csv`. The CSV has the following columns: `row_id`, `timestamp`, `sensor_name`, `value`.
2. A scanned image of the quality control specification sheet located at `/app/specs.png`. 

Your task is to build a Rust-based ETL pipeline that performs the following steps:

1. **Information Extraction**: Extract the textual data from `/app/specs.png`. (You may use standard tools like `tesseract`, which is available in your environment, to perform OCR on this image). The image contains the expected Mean, expected Standard Deviation, and the Sigma threshold (Z-score limit) for flagging anomalies for two critical sensors: `Pressure_Sensor` and `Temp_Sensor`.

2. **Rust ETL Implementation**: Create a new Rust project in `/home/user/etl_pipeline`. Write a Rust program that:
   - Reads the constraints you extracted from the OCR step.
   - Streams the data from `/home/user/data/readings.csv`.
   - Performs data validation and anomaly detection: For each row, calculate if the `value` is an anomaly. A value is an anomaly if the absolute difference between the `value` and the sensor's expected Mean is strictly greater than `Sigma_Threshold * Standard_Deviation`.
   - Ignore readings from sensors that are not explicitly mentioned in the specification sheet.

3. **Output**: Your Rust program must output a JSON file located at `/home/user/anomalies.json`. This file must contain a single JSON array of integers representing the `row_id`s of all detected anomalies, sorted in ascending order.
   Example format: `[12, 45, 102, 3409]`

Build and execute your Rust program so that the final `/home/user/anomalies.json` is generated. The automated test will read your output and compare it against the hidden ground truth of anomalies using an F1 score metric.