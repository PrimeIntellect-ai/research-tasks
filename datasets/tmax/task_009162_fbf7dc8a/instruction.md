You are a data analyst working with sensor telemetry. You have been given a wide-format CSV file located at `/home/user/raw_sensors.csv` containing reading data from various devices. 

The input file has a header and is formatted as:
`device_id,region,t1,t2,t3,t4`

Your goal is to write a purely Bash-based pipeline (using tools like `awk`, `sed`, `coreutils`, etc. - no Python/Perl) saved as an executable script at `/home/user/process.sh`. When executed, the script must read `/home/user/raw_sensors.csv` and generate an output file at `/home/user/alerts.csv` by applying the following steps:

1. **Wide-to-Long Format Reshaping:** Convert the wide table into a long format. Each `device_id` and `region` should have a separate row for each time period (`t1`, `t2`, `t3`, `t4`). Skip the header line. The intermediate long format should be conceptually: `device_id,region,time_period,value`.
2. **Feature Extraction:** Append a 5th column called `alert_level`. If the numeric `value` is strictly greater than `50.0`, the `alert_level` is `CRITICAL`. Otherwise, it is `NORMAL`.
3. **Hash-Based Anonymization:** Replace the `device_id` in the first column with an 8-character MD5 hash of the original `device_id` string (compute the MD5 hash of the string without a newline, e.g., using `echo -n`, and extract the first 8 hex characters).
4. **Stratified Sampling & Deduplication:** Filter the dataset to include ONLY records with a `CRITICAL` alert level. Furthermore, to avoid alert fatigue, we only want to keep exactly **ONE** `CRITICAL` record per `region`. If a region has multiple critical records, keep the one that appeared earliest in the file (scanning left-to-right through the columns `t1` to `t4`, then moving to the next row).

The final output file `/home/user/alerts.csv` must be a comma-separated file with no header, containing the filtered and anonymized rows. 

Format of final rows:
`hashed_device,region,time_period,value,alert_level`