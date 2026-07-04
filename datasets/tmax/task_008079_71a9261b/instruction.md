You are a log analyst investigating patterns in server thermal performance. We have a sensor logging system that records server temperature and CPU load every minute, but the logging agent occasionally crashes, leaving gaps in the data.

Your task is to build an automated data processing pipeline in **C** that cleans the data, computes rolling statistics, detects cooling system anomalies, and prepares a deployment script and cron schedule for automated execution.

**Step 1: Write the C Analyzer (`/home/user/analyzer.c`)**
Write a C program that reads a CSV file named `/home/user/sensor_data.csv`.
The CSV has no header and contains three comma-separated columns:
`TIMESTAMP, TEMPERATURE, CPU_LOAD` (integer Unix timestamp, float temperature, integer CPU load percentage).

Your C program must perform the following:
1. **Resampling and Gap-filling**: The logs should have exactly one entry per minute (i.e., timestamp increments of 60). If there are missing timestamps between consecutive rows, fill the gaps by repeating the temperature and CPU load of the *immediately preceding* valid row for every missing 60-second interval. 
2. **Rolling Statistics**: Compute a 5-minute rolling average of the temperature (i.e., the average of the current minute and the previous 4 minutes). This includes the gap-filled minutes. For the first 4 minutes, compute the average using whatever data is available so far (1 to 4 points).
3. **Anomaly Detection**: After gap-filling and computing the 5-minute rolling average, check for a cooling anomaly. A cooling anomaly is defined as:
   - The 5-minute rolling average temperature is strictly greater than `80.0`.
   - The CPU load (at that specific minute) is strictly less than `50` (implying the server is hot despite low load).
4. **Pipeline Logging**: For every detected anomaly, append a single line to `/home/user/anomalies.log` in the exact format:
   `TIMESTAMP: <timestamp>, AVG_TEMP: <avg_temp_formatted_to_2_decimal_places>, CPU: <cpu_load>`
   (e.g., `TIMESTAMP: 1620000300, AVG_TEMP: 82.50, CPU: 20`)

Compile your C code into an executable named `/home/user/analyzer`. Use standard libraries only (`stdio.h`, `stdlib.h`, `string.h`, etc.).

**Step 2: Deployment and Scheduling**
1. Create a bash wrapper script at `/home/user/run_pipeline.sh` that safely executes `/home/user/analyzer`. Ensure it is executable.
2. Create a cron configuration file at `/home/user/crontab.txt` that schedules `/home/user/run_pipeline.sh` to run every 5 minutes (using standard cron syntax, with no environment variables or user fields, just the schedule and the command).

Ensure the C program successfully runs and processes the existing `/home/user/sensor_data.csv` so that `/home/user/anomalies.log` is generated before you finish.