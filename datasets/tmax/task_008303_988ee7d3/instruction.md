You are a data analyst tasked with processing a corrupted sensor log file. 

You have been provided with a raw log file at `/home/user/sensor_data.csv`. The system that generated this file had a bug, causing the timestamps and numerical values to be embedded within unstructured, garbage text. There are also significant gaps in the data where the sensor went offline.

Your objective is to build a Python-based data processing pipeline that extracts the valid data, cleans it, resamples it to a strict hourly frequency, fills in the missing gaps mathematically, and outputs a clean CSV.

Here are your specific requirements:
1. **Extraction (Regex):** Read `/home/user/sensor_data.csv`. Use regular expressions to extract the timestamp and the temperature value from each row. 
    * The timestamps are hidden inside brackets in the `raw_log` column (e.g., `...[YYYY-MM-DD HH:MM:SS]...`).
    * The temperatures are embedded in the `raw_value` column, always preceded by `T:` and followed by a character (e.g., `...T:23.5C...`).
    * Drop any rows where valid timestamps or temperature values cannot be extracted.

2. **Resampling & Gap-Filling:** 
    * Convert the extracted timestamps into a proper datetime index.
    * Resample the dataset to an exact **1-Hour (1H)** frequency. If there are multiple readings in the same hour, take their mean.
    * You will notice missing hourly periods (gaps) in the resampled data. You must use **linear interpolation** to fill in the missing temperature values for these gaps.

3. **Output:** 
    * Save the final processed dataset to `/home/user/processed_hourly.csv`.
    * The output CSV must have exactly two columns: `timestamp` and `temperature`.
    * The `timestamp` column must be formatted as `YYYY-MM-DD HH:MM:SS`.
    * The `temperature` column must be rounded to exactly 1 decimal place (e.g., `14.0`).
    * Do not include the pandas index in the CSV output unless it is named `timestamp` and serves as the first column.

Please execute the necessary code to produce the final output file.