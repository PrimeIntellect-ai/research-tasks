You are a data engineer responsible for processing IoT sensor telemetry. You have been given a raw dataset at `/home/user/raw_sensor.csv` containing environmental readings. The pipeline requires cleaning the data, stratifying it, and computing mathematical rolling statistics using a custom C++ program, finally orchestrating this as a scheduled ETL job.

Perform the following tasks:

1. **Data Cleaning and Stratification (Bash/Standard CLI)**
   Write a script `/home/user/pipeline.sh` that starts by preprocessing `/home/user/raw_sensor.csv`.
   The input format is: `timestamp,sensor_id,sensor_type,value`
   Your script must:
   - Remove any rows where the `value` is missing or empty.
   - Deduplicate rows (if all four columns are exactly identical, keep only one).
   - Filter the data to keep *only* rows where `sensor_type` is `temp`.
   - Sort the resulting records chronologically by `timestamp` (oldest first).
   - Save this cleaned, sorted, temp-only data to `/home/user/temp_cleaned.csv`.

2. **Rolling Statistics Computation (C++)**
   Write a C++ program at `/home/user/rolling_stats.cpp`. 
   The `pipeline.sh` script must compile this C++ program to `/home/user/rolling_stats` (using `g++ -O3`) and execute it.
   The C++ program must:
   - Read `/home/user/temp_cleaned.csv`.
   - For each unique `sensor_id`, compute a rolling mean and rolling population standard deviation of the `value` column over a window of exactly 5 consecutive readings (ordered by timestamp).
   - Do not output anything for a `sensor_id` until it has accumulated at least 5 readings.
   - For the 5th reading and every subsequent reading, output a row with the format:
     `timestamp,sensor_id,rolling_mean,rolling_stddev`
   - Both `rolling_mean` and `rolling_stddev` must be rounded to exactly 2 decimal places (e.g., `24.50`).
   - Write the final output to `/home/user/stats_output.csv` (do not include a header row in the output).

3. **Pipeline Scheduling**
   - Ensure `/home/user/pipeline.sh` has executable permissions.
   - Create a cron configuration file at `/home/user/cron_schedule.txt` that schedules `/home/user/pipeline.sh` to run every 15 minutes exactly (i.e., at minutes 0, 15, 30, and 45 past every hour).
   - Load this file into the user's crontab using the `crontab` command.

All files must be created in `/home/user`. Ensure your C++ code handles standard edge cases like standard deviation of a zero-variance window without returning NaN ungracefully (it should output `0.00`).