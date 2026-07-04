You are a data engineer tasked with building a time-series ETL pipeline for industrial IoT sensors. We receive daily sensor readings, but the data feed is faulty and often sends exact duplicate records. Additionally, we need to monitor these sensors for deviations from a known baseline daily pattern.

Your objective is to build a multi-stage pipeline using Python and Bash, and schedule it. 

Here are the detailed requirements:

**1. Directory Structure & Input Data**
You have the following files and directories (already existing):
- `/home/user/raw_data/sensors_20231001.csv` : The raw time-series data for October 1st, 2023. Format: `timestamp,sensor_id,value`. (Timestamps are in ISO 8601 format, e.g., `2023-10-01T00:00:00Z`).
- `/home/user/reference/baseline.json` : A JSON list of 24 floating-point numbers representing the ideal 24-hour reading pattern.
- `/home/user/clean_data/` : An empty directory for deduplicated output.
- `/home/user/metrics/` : An empty directory for the final metrics output.

**2. Stage 1: Hash-Based Deduplication (Python)**
Write a Python script `/home/user/dedup.py` that reads the raw CSV file.
- It must implement **hash-based deduplication**: for each row, compute the MD5 hash of the concatenated string of `timestamp,sensor_id,value`.
- Keep only the first occurrence of each hash.
- Write the deduplicated data to `/home/user/clean_data/sensors_20231001_clean.csv`, maintaining the original CSV header (`timestamp,sensor_id,value`).
- Sort the output CSV primarily by `sensor_id` (ascending) and secondarily by `timestamp` (ascending).

**3. Stage 2: Distance Computation (Python)**
Write a Python script `/home/user/compute_metrics.py` that reads the deduplicated CSV and the baseline JSON.
- Group the data by `sensor_id`. (Assume each sensor has exactly 24 chronological readings after deduplication).
- For each sensor, compute the **Euclidean distance** between its 24 hourly readings and the 24 values in the baseline JSON.
- Output the results to `/home/user/metrics/distances.csv`.
- The output format must be exactly `sensor_id,distance` with a header row.
- Round the distance to exactly 2 decimal places. Sort the file by `sensor_id` in ascending alphabetical order.

**4. Stage 3: Orchestration (Bash)**
Create a shell script `/home/user/run_pipeline.sh` that:
- Executes `/home/user/dedup.py`
- Then executes `/home/user/compute_metrics.py` if the first script succeeds.
- Make sure this script is executable.

**5. Stage 4: Scheduling (Cron)**
Set up a cron job for the current user (`user`) that runs `/home/user/run_pipeline.sh` exactly at midnight (00:00) every day. The cron job should simply execute the script (do not worry about passing specific dates for this exercise; assume the scripts hardcode or discover the files as you've written them). Use `crontab` to install this schedule.

Complete these tasks. The automated test will verify the contents of `/home/user/clean_data/sensors_20231001_clean.csv`, `/home/user/metrics/distances.csv`, and your installed crontab.