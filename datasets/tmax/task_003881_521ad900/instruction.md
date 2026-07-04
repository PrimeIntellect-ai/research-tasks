You are a Data Engineer building an ETL pipeline to process raw IoT sensor data. 

We have a raw dataset located at `/app/raw_sensors.csv`. It contains two columns: `timestamp` and `raw_value`. The timestamps are messy and come in various formats (e.g., RFC3339, custom string formats like "02 Jan 06 15:04 MST", Unix timestamps).

Additionally, the calibration parameters for this sensor are only available as a scanned image at `/app/calibration.png`. You will need to extract the parameters from this image (you can use `tesseract` which is preinstalled) to process the data.

Your goal is to write a Go program (e.g., `pipeline.go`) that performs the following pipeline steps:
1. **Parameter Extraction**: Extract the `OFFSET`, `SCALE`, and `WINDOW` values from the calibration image.
2. **Timestamp Alignment**: Parse all timestamps in `/app/raw_sensors.csv` and normalize them to RFC3339 format. Sort the records chronologically.
3. **Normalization**: Apply the calibration to each raw value: 
   `normalized_value = (raw_value + OFFSET) * SCALE`
4. **Rolling Statistics**: Compute a Simple Moving Average (SMA) of the `normalized_value` over the last `WINDOW` records (including the current record). For the first `WINDOW-1` records, average whatever records are available up to that point.
5. **Output**: Write the results to `/app/clean_output.csv` with exactly two columns: `time` (RFC3339 formatted) and `smoothed_value` (formatted to 4 decimal places).

The final verification will evaluate the Mean Squared Error (MSE) of your `smoothed_value` column against a hidden reference dataset. Your MSE must be less than 0.001. 

Please execute your workflow and generate the `/app/clean_output.csv` file.