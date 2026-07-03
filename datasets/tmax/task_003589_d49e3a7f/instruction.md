You are a data engineer tasked with building an ETL pipeline to process raw, multilingual weather sensor logs. The raw data is located at `/home/user/raw_sensors.tsv`.

The file is tab-separated with the following columns:
1. `Timestamp`: Unix epoch time (integer).
2. `Location`: Sensor location name, which may include various Unicode characters (e.g., "Paris/Île-de-France", "Tokyo/東京").
3. `Temperature`: Temperature reading (float).
4. `Status`: A text field that sometimes contains garbage or error codes (e.g., "OK", "ERR: low battery"). We only want to process records where the status is exactly "OK".

Your objective is to clean, normalize, group, resample, and gap-fill this data. You must write a C program (`/home/user/resample.c`) to handle the resampling and gap-filling logic, and you may use standard Bash utilities (like `sort`, `awk`, `grep`) to preprocess the data before feeding it to your C program.

Requirements:
1. **Filtering & Cleaning**: Extract only the records where the `Status` is exactly "OK".
2. **Sorting & Grouping**: Group the data by `Location` and order it chronologically by `Timestamp`.
3. **Resampling**: Aggregate the timestamps into hourly intervals (i.e., round the Unix timestamp down to the nearest multiple of 3600). If multiple valid readings exist for the same location in the same hour, calculate the average temperature for that hour.
4. **Gap-Filling**: For each location, if there are missing hourly intervals between its earliest and latest recorded hours, fill in the missing hours. The temperature for a missing hour should be the temperature of the *most recent previous valid hour* for that location (forward-fill).
5. **Output**: Your final pipeline should output the processed data to `/home/user/processed_sensors.tsv` with the format:
   `Location\tTimestamp\tTemperature`
   The `Temperature` must be formatted to exactly two decimal places (e.g., `15.50`). The output should be sorted alphabetically by Location (by raw byte values), and then chronologically by Timestamp.

Write a shell script `/home/user/run_pipeline.sh` that compiles your C program and executes the full pipeline to generate the final output file. Ensure your C program can handle arbitrary UTF-8 strings for the location.