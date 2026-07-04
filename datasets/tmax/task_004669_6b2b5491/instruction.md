You are an AI assistant acting as a Data Engineer.

We have an upstream ETL job that occasionally fails and retries, which has resulted in duplicate records in our latest batch. Additionally, the sensor pipeline drops some values, requiring imputation, and a faulty sensor calibration event has introduced high-value anomalies.

Your task is to write a Bash script at `/home/user/process_etl.sh` that processes this data and generates a summary report.

**Input Files:**
1. `/home/user/etl_data.csv` - The raw data file with header `timestamp,record_id,sensor_value`.
2. `/home/user/report_template.txt` - A template file containing placeholders for the final report.

**Processing Requirements:**
1. **Deduplication:** Sort the data chronologically by `timestamp`. Remove duplicate rows based solely on `record_id`. If a `record_id` appears multiple times, keep only the first occurrence chronologically.
2. **Imputation:** Some `sensor_value` fields are empty (e.g., `2023-10-01T10:01:00,A2,`). Use a forward-fill strategy to impute missing values (replace the empty value with the most recently observed valid `sensor_value` from the chronologically sorted, deduplicated records). The very first record is guaranteed to have a valid value.
3. **Anomaly Detection:** An anomaly is defined as any record where the final (imputed or original) `sensor_value` is strictly greater than `100.0`. Count the total number of anomalies.
4. **Aggregation:** Calculate the mean of all final `sensor_value`s across the deduplicated dataset. Round this average to exactly two decimal places (e.g., `63.14`).
5. **Template Generation:** Read `/home/user/report_template.txt` and replace the exact string `{{AVG_VALUE}}` with the calculated average, and `{{ANOMALY_COUNT}}` with the integer count of anomalies.
6. **Output:** Save the finalized text to `/home/user/final_report.txt`.

Ensure your script `/home/user/process_etl.sh` is executable and can be run without arguments to produce the `/home/user/final_report.txt` file. You may use standard Unix text processing utilities (like `awk`, `sed`, `grep`, `sort`, `bc` or inline `python`) within your Bash script.