You are a data analyst tasked with processing a batch of time-series sensor data. 

In the directory `/home/user/sensor_data/`, there are several CSV files containing temperature and humidity readings. The expected CSV format is exactly four columns: `timestamp,sensor_id,temperature,humidity`.

However, the data pipeline upstream had some issues. Some files might be exact duplicates of each other, and some files might be corrupted (having missing columns on some rows).

Write and execute a Bash data processing pipeline that performs the following steps:

1. **Hash-based Deduplication**: Identify identical files in `/home/user/sensor_data/` based on their MD5 hash. Keep one copy of each unique file and delete the duplicates.
2. **Quality Gate**: Validate the remaining CSV files. A valid file must have exactly 4 comma-separated columns on every line (including the header). If a file has any line with fewer or more than 4 columns, move it to the directory `/home/user/invalid_data/` (create this directory if it doesn't exist).
3. **Consolidation**: Concatenate the valid CSV files into a single stream, ensuring there is exactly one header row at the top.
4. **Stratified Sampling**: Sort the consolidated data records by `sensor_id` (ascending) and then by `timestamp` (ascending). For each unique `sensor_id`, perform data sampling by keeping only the 1st, 11th, 21st, etc., chronologically ordered record for that sensor.
5. **Output**: Save the final sampled dataset (including the header) to `/home/user/sampled_data.csv`.

Ensure your final CSV has the correct header and the sampled rows match the sorting and sampling logic described. Do not use external Python scripts; rely entirely on Bash, `awk`, `sort`, and standard coreutils.