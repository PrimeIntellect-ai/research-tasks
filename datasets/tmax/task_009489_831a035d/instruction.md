You are a data analyst working for a meteorological agency. We have received a batch of messy sensor logs in `/home/user/sensor_logs/`. There are 4 files: `sensor_1.csv`, `sensor_2.csv`, `sensor_3.csv`, and `sensor_4.csv`.

Your task is to write a Python script at `/home/user/process_sensors.py` and run it to process these files. The script must meet the following requirements:

1. **Parallel Data Processing:** The script must process all CSV files concurrently using Python's `multiprocessing` or `concurrent.futures.ProcessPoolExecutor` to speed up the workflow.
2. **Regex Pattern Construction:** Each CSV has three columns: `Log_Time`, `Raw_Payload`, and `QC_Flag`. The `Raw_Payload` contains unstructured text. Use regex to extract two numerical values: Temperature and Pressure. 
   - The payload format looks like: `... T:<temperature>C ... P:<pressure>hPa ...` (e.g., `DATA_T:23.4C_STATUS_P:1012hPa_END`). 
   - If a payload has `ERR` instead of a number (e.g., `T:ERR`), treat it as a missing value (NaN).
3. **Validation Checkpoints:** Filter the data *before* processing:
   - Only keep rows where `QC_Flag` is exactly `PASS`.
   - Discard rows that do not match the `PASS` flag.
4. **Interpolation and Imputation:**
   - Sort the valid data for each sensor chronologically by `Log_Time` (which is an integer Unix timestamp).
   - For missing Temperature values, use **forward fill** (propagate the last valid observation forward). 
   - For missing Pressure values, use **linear interpolation** with respect to the sequence (treat as equally spaced for the interpolation).
   - If any missing values remain at the very beginning of the series (which cannot be forward-filled or interpolated easily), drop those specific rows.
5. **Output generation:**
   - Combine the cleaned, imputed data from all sensors into a single file at `/home/user/cleaned_telemetry.csv`.
   - The output CSV must have exactly these columns in order: `Sensor_ID` (e.g., `sensor_1`), `Log_Time`, `Temperature`, `Pressure`.
   - Sort the final combined CSV by `Sensor_ID` (alphabetically) and then by `Log_Time` (ascending).
   - Ensure all numerical values are rounded to 2 decimal places.

Run your script to produce `/home/user/cleaned_telemetry.csv`.