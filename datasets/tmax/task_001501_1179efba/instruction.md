As an automation specialist, you are tasked with building a robust data processing pipeline to clean, calibrate, and reshape a dataset of raw sensor readings. 

We have a corrupted JSON Lines file located at `/app/data/raw_sensors.jsonl`. Unfortunately, the logging system that produced this file had a bug: it often wrote malformed unicode escape sequences (e.g., writing `\u00` instead of `\u0000`, or leaving incomplete `\u` sequences) which causes standard JSON parsers to crash. 

Furthermore, the sensors require mathematical calibration before the data is useful. The calibration formula and coefficients are not stored in code; they were provided in a scanned specification image located at `/app/calibration_specs.png`. 

Your workflow must accomplish the following using Python:
1. **Information Extraction**: Use OCR (e.g., `pytesseract` which is available in the environment) to read `/app/calibration_specs.png` and extract the linear calibration formula (it will be in the form `y = M * x + C`).
2. **Cleaning & Parsing**: Parse `/app/data/raw_sensors.jsonl`, automatically cleaning or discarding the broken unicode escape sequences so the valid data can be extracted.
3. **Reshaping**: The JSON data is in a "wide" format: `{"timestamp": "2023-10-01T10:00:05Z", "s1": 12.4, "s2": 15.1, "s3": 8.9}`. Reshape this into a "long" format dataset containing `timestamp`, `sensor_id`, and `raw_value`.
4. **Calibration**: Apply the mathematical formula extracted from the image to convert `raw_value` into a calibrated `cal_value`.
5. **Timestamp Alignment & Deduplication**: Align all timestamps by rounding down to the nearest minute. If there are multiple readings for the same `sensor_id` in the same minute, aggregate them by calculating the mathematical average (mean) of the `cal_value`. 
6. **Parallel Processing**: The pipeline must use Python's `multiprocessing` or `concurrent.futures` to process the data in parallel across multiple CPU cores to ensure scalability for large datasets.

Save your final processed dataset as a CSV file to `/app/processed_data.csv`. The CSV must have exactly these columns: `minute_timestamp` (in ISO 8601 format, e.g., `2023-10-01T10:00:00Z`), `sensor_id`, and `calibrated_mean` (rounded to 3 decimal places).

An automated test will compute the Mean Squared Error (MSE) between your `calibrated_mean` values and our hidden reference dataset. Your solution must achieve an MSE of less than 0.01.