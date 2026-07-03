You are a data scientist tasked with cleaning and validating a batch of legacy sensor data from an environmental monitoring network. 

First, you must extract calibration specifications from a scanned reference document located at `/app/calibration_specs.png`. This image contains a table with sensor IDs, their valid minimum values, maximum values, and a scale multiplier. You will need to use OCR (e.g., `pytesseract`, which is installed) to read this table programmatically.

Next, you need to build an automated data sanitization pipeline. Write a Python script at `/home/user/process_sensors.py` that conforms to the following CLI signature:
`python3 /home/user/process_sensors.py --input <input_directory> --output <accepted_directory> --reject <rejected_directory>`

The script must perform the following operations on every file in the `<input_directory>`:
1. **Multi-format Support:** Read files in both CSV and JSON formats.
2. **Schema & Value Validation:** 
   - Extract the `Sensor_ID` and check if it matches one of the sensors in your extracted calibration specs.
   - Discard the file entirely (move it to `<rejected_directory>`) if it contains unrecognized sensors, corrupted structural schemas, or if *any* value falls outside the (Min_Val, Max_Val) range defined in the calibration image.
3. **Cleaning & Interpolation:** For files that pass validation, apply the scale multiplier to all numeric readings. Missing readings (represented as `null`, `""`, or `NaN`) must be filled using linear interpolation based on surrounding values in the time series.
4. **Output:** Save the accepted and cleaned data into `<accepted_directory>` as normalized CSV files (columns: `timestamp`, `Sensor_ID`, `value`), keeping the original base filename but changing the extension to `.csv`. 

Your script will be tested against two datasets. Ensure it is robust enough to accept perfectly clean data (even if it requires interpolation) and strictly reject malformed, out-of-bounds, or maliciously corrupted data.