You are a data engineer responsible for cleaning and transforming raw telemetry data from industrial temperature sensors. The data is currently stored in a pipe-delimited text file, but it suffers from noise (invalid readings) and missing transmissions.

Your task is to build an ETL script (using standard Linux tools, Bash, AWK, or Python) to validate, clean, gap-fill, and normalize this dataset.

**Input Data:**
File: `/home/user/raw_telemetry.txt`
Format: `sensor_id|timestamp_epoch|temp_celsius`
Example row: `A1|1700000000|15.5`

**Processing Requirements:**
1. **Validation:** Read the input file and discard any rows where the `temp_celsius` reading is completely invalid. Valid temperatures are defined as strictly between `-20.0` and `60.0` (inclusive). So, `>= -20.0` and `<= 60.0`.
2. **Gap-Filling (Resampling):** The sensors are supposed to report exactly every 60 seconds. After removing invalid data, some sensors will have missing epochs. 
   - Group the valid data by `sensor_id`.
   - For each `sensor_id`, identify its minimum and maximum `timestamp_epoch` (from the valid rows).
   - Generate a continuous 60-second interval time series between that min and max timestamp.
   - If a timestamp is missing in the valid data, fill the missing `temp_celsius` using **forward-fill** (i.e., use the temperature from the most recent preceding valid timestamp for that sensor).
3. **Normalization & Sorting:** 
   - Convert the output delimiter from a pipe `|` to a comma `,`.
   - The final output columns must be `sensor_id,timestamp_epoch,temp_celsius`.
   - Sort the final output first by `sensor_id` ascending (alphabetically), then by `timestamp_epoch` ascending (numerically).

**Output:**
Save the final processed data to: `/home/user/processed_telemetry.csv`

Ensure your script handles everything end-to-end and creates the exact output file requested.