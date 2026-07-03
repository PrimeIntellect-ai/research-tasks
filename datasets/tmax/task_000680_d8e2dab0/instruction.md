You are an automation specialist tasked with building a robust data processing pipeline for a network of IoT sensors. You need to process a raw data extract, deduplicate it using a hash-based mechanism, aggregate the results, log the process, and prepare a cron schedule for the pipeline.

The raw data is located at `/home/user/data/raw/sensor_data.csv` (which already exists). 
It has the following columns: `id,timestamp,sensor,value`

Your task is to write a Python script at `/home/user/process.py` that performs the following steps:
1. **Hash-based deduplication**: Read the CSV file. For each row, compute an MD5 hash of the string formatted exactly as `timestamp|sensor|value` (omitting the `id`). Use this hash to identify and remove duplicates. Keep only the first occurrence of each unique hash.
2. **Sorting and Grouping**: Sort the deduplicated records by `sensor` alphabetically, and then by `timestamp` in ascending order. Group the records by `sensor` and calculate the total number of events and the average `value` (rounded to 1 decimal place) for each sensor.
3. **Output**: Save the grouped data to `/home/user/data/processed/grouped.csv` with columns exactly as: `sensor,event_count,avg_value`.
4. **Logging**: Append a log entry to `/home/user/logs/run.log` upon completion. The log must be exactly in this format: `[YYYY-MM-DD HH:MM:SS] Processed <N> unique records, dropped <M> duplicates.` (where `<N>` is the number of unique records kept, and `<M>` is the number of duplicate records dropped).

After writing and successfully running your script, create a cron job definition file at `/home/user/schedule.cron`. This file should contain exactly one line: the crontab entry required to run `/usr/bin/python3 /home/user/process.py` every Sunday at midnight (00:00). 

*Note: Ensure the output directories exist before writing to them. You may use any standard library in Python. Do not install any external pip packages.*