You are a data engineer tasked with fixing and scaling an ETL pipeline in Bash that performs anomaly detection on sensor data. 

Currently, the data pipeline has a silent data corruption issue: the downstream analytics tools treat missing values (empty fields in the CSV) as `0`, which artificially drags down the mean and variance statistics, causing false anomalies. 

Your objectives are:
1. **Environment Setup**: Ensure `datamash` and `jq` are installed on the system (using `sudo apt-get` if necessary; password for `user` is `user`, or run as root if configured). Note: you have standard user privileges but can use `sudo`.
2. **Fix the ETL Script (`/home/user/pipeline/detect.sh`)**:
   Write a Bash script `detect.sh` that takes two arguments: an input CSV file and a threshold multiplier (integer).
   The input CSV (`/home/user/pipeline/sensor_data.csv`) has a header `timestamp,value`.
   The script must:
   - Calculate the true mean of the `value` column, *strictly ignoring* any rows where `value` is empty. Round the mean to the nearest integer.
   - Calculate the Mean Absolute Deviation (MAD) of the `value` column. When calculating MAD, assume any missing values are replaced by the *mean* calculated in the previous step. Round the MAD to the nearest integer.
   - Output the number of anomalies found. An anomaly is defined as any row where the absolute difference between its value (after imputing missing values with the mean) and the mean is strictly greater than `threshold * MAD`.
   - The script should print ONLY the integer count of anomalies to standard output.
3. **Hyperparameter Tuning & Experiment Tracking (`/home/user/pipeline/sweep.sh`)**:
   Write a script `sweep.sh` that performs a parameter sweep across threshold values `1`, `2`, `3`, `4`, and `5`.
   For each threshold:
   - Run `detect.sh` on `/home/user/pipeline/sensor_data.csv`.
   - Benchmark the execution time of `detect.sh` for that run using the `date +%s%3N` (milliseconds) command before and after the call.
   - Save the results as a JSON array in `/home/user/pipeline/experiments.json` with the following structure:
     ```json
     [
       {
         "threshold": 1,
         "anomalies": 12,
         "time_ms": 45
       },
       ...
     ]
     ```

**Important Notes:**
- Do not use Python, R, or Perl for the data processing; you must use Bash along with standard POSIX utilities (like `awk`, `sed`, `grep`, `datamash`, `bc`, etc.).
- Ensure your output file is located exactly at `/home/user/pipeline/experiments.json`.
- Missing values in the CSV are represented as empty strings after the comma (e.g., `2023-01-01T10:00:00,`).