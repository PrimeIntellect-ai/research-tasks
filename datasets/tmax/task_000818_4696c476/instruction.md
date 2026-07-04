You are a data scientist tasked with building a robust data cleaning and transformation pipeline for an array of IoT sensors. You have a set of legacy wide-format CSV datasets, but they are polluted with corrupted data.

Your goal is to create a Python script at `/home/user/cleaner.py` that processes a single CSV file and outputs a cleaned, reshaped CSV file. The script must be invoked as:
`python3 /home/user/cleaner.py <input.csv> <output.csv>`

**Requirements:**

1. **Anomaly Detection (The Filter):**
   There is a legacy quality-control tool located at `/app/legacy_qc`. This tool is a compiled, stripped binary that takes a CSV file path as an argument and exits with code `1` if the file contains corrupted/evil data, and `0` if it is clean.
   Because calling this binary via subprocess is too slow for our streaming architecture, you must reverse-engineer or black-box test `/app/legacy_qc` to determine its exact anomaly-detection logic, and reimplement this logic natively in your Python script.
   If your script detects a corrupted file (based on the reimplemented logic), it MUST exit with status code `1` immediately, without writing any output CSV.

2. **Time Series Reshaping & Resampling:**
   If the file is clean, your script must:
   - Read the wide-format CSV. The input format has columns: `timestamp`, `sensor_alpha`, `sensor_beta`, `sensor_gamma`.
   - Convert the `timestamp` column to proper datetime objects.
   - Reshape the data from wide to long format (columns should be exactly: `timestamp`, `sensor_name`, `value`).
   - Resample the time series for each sensor to regular 5-minute intervals, starting from the earliest timestamp in the file.
   - Forward-fill any missing values (gaps) up to a maximum of 3 consecutive intervals. Any remaining `NaN` values should be filled with `0.0`.
   - Save the result to the `<output.csv>` path provided in the arguments. The script must then exit with status code `0`.

3. **Pipeline Logging:**
   For every clean file successfully processed, append a log entry to `/home/user/processing.log` in the exact format:
   `[SUCCESS] Processed <input_filename>: original_rows=<N>, final_rows=<M>`
   (Where `<input_filename>` is just the basename of the file).

You have access to sample datasets in `/home/user/samples/` to help you test and deduce the logic of `/app/legacy_qc`.