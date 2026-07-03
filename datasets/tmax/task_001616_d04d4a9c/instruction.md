You are an automation specialist tasked with building a lightweight ETL and reporting pipeline for a network of IoT climate sensors. The sensors occasionally drop data packets, resulting in missing values. You need to impute these missing values, generate a formatted report, and schedule this process.

Because this runs on a minimal edge device, you **must use pure Python (standard library only, no Pandas or NumPy)** for the data processing.

Here is the setup:
You have an input file at `/home/user/input/raw_sensor.csv` (which you should assume exists when your scripts run, but you should test your code with the sample data provided below).
```csv
timestamp,temperature,humidity
2023-10-01T10:00:00,22.5,45.0
2023-10-01T10:05:00,,46.0
2023-10-01T10:10:00,23.5,
2023-10-01T10:15:00,24.0,48.0
```

There is also a report template at `/home/user/input/report_template.txt`:
```text
Daily Sensor Report
-------------------
Temperature: Min {{TEMP_MIN}}, Max {{TEMP_MAX}}, Avg {{TEMP_AVG}}
Humidity: Min {{HUM_MIN}}, Max {{HUM_MAX}}, Avg {{HUM_AVG}}
```

**Phase 1: Data Imputation & Template Generation (Python)**
Write a Python script at `/home/user/process_sensor.py` that does the following:
1. Reads `/home/user/input/raw_sensor.csv`.
2. Performs **linear time-based interpolation** to fill in the missing `temperature` and `humidity` values. You must calculate the missing value by linearly interpolating between the nearest preceding and nearest succeeding valid values based on the time difference. (Assume the first and last rows will never have missing values).
3. Calculates the Minimum, Maximum, and Average for the *interpolated* (complete) dataset for both temperature and humidity.
4. Reads `/home/user/input/report_template.txt`.
5. Replaces the placeholders (`{{TEMP_MIN}}`, `{{TEMP_MAX}}`, `{{TEMP_AVG}}`, `{{HUM_MIN}}`, `{{HUM_MAX}}`, `{{HUM_AVG}}`) with the calculated values. All replaced numeric values must be formatted to exactly **two decimal places** (e.g., `23.50`).
6. Saves the completed report to `/home/user/output/report.txt`.

**Phase 2: Pipeline Wrapper (Bash)**
Write a bash script at `/home/user/run_pipeline.sh` that:
1. Creates the `/home/user/output` directory if it does not exist.
2. Executes `/home/user/process_sensor.py`.
3. Ensure this script is executable (`chmod +x`).

**Phase 3: Scheduling (Cron)**
Install a crontab for the `user` that schedules `/home/user/run_pipeline.sh` to run **every 15 minutes** (e.g., at 0, 15, 30, and 45 past the hour). 

To complete the task:
1. Create the input files `/home/user/input/raw_sensor.csv` and `/home/user/input/report_template.txt` with the exact content provided above.
2. Write your scripts (`process_sensor.py` and `run_pipeline.sh`).
3. Set up the crontab.
4. Execute `/home/user/run_pipeline.sh` once manually so the output file is generated for verification.