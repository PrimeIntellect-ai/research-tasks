You are a data engineer responsible for processing streaming sensor logs. We have a raw log file located at `/home/user/raw_sensors.txt`. 

Your task is to build a Bash-based ETL pipeline script at `/home/user/etl.sh` that performs the following steps:
1. **Filter**: Stream the log file and extract only the records for `DEVICE_A`.
2. **Feature Extraction & Timestamp Alignment**: Extract the timestamp (truncated to the minute) and the `TEMP` value. If there are multiple readings for `DEVICE_A` within the exact same minute, keep only the **last** reading for that minute.
3. **Resampling & Gap-Filling**: Ensure the output has exactly one record for every minute between `2023-10-01 10:00` and `2023-10-01 10:10` (inclusive). If a minute has no data for `DEVICE_A`, perform a forward-fill (use the temperature value from the most recent previous minute). You can assume the first minute (`10:00`) always has a reading.
4. **Format**: Output the final cleaned data to `/home/user/clean_temperature.csv` in the format `YYYY-MM-DD HH:MM,TEMP`.

Example of raw log format:
`[2023-10-01 10:00:15] DEVICE_A TEMP=22.5`
`[2023-10-01 10:00:45] DEVICE_B TEMP=21.0`

Requirements:
- Write the entire pipeline using standard Linux text processing tools (e.g., `awk`, `sed`, `grep`, `bash`).
- Do not use Python, Perl, or any non-Bash scripting language.
- Run your script to generate `/home/user/clean_temperature.csv`.