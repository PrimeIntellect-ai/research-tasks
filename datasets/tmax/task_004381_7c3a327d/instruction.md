You are an automation specialist managing a legacy ETL pipeline. An ETL job failed midway and automatically retried, resulting in a dump file that contains duplicated records. Furthermore, some sensor readings were dropped during transit, and the event descriptions are messy. 

Your task is to create a Bash-only pipeline (you may use standard tools like `awk`, `sed`, `grep`, `sort`, `tr`, etc., but NO Python, Perl, or Ruby) to process the file `/home/user/etl_dump.csv`.

Here are the processing requirements:
1. **Deduplication & Ordering**: The input has a header `timestamp,sensor_value,event_description`. Sort the data chronologically by `timestamp` (ascending). Remove any exact duplicate rows caused by the ETL retry. 
2. **Imputation**: The `sensor_value` column contains float values, but some are marked as `MISSING`. You must forward-fill these missing values (replace `MISSING` with the most recently observed valid `sensor_value` chronologically). The first chronological record is guaranteed to have a valid float value.
3. **Normalization**: The `event_description` field contains mixed-case text with punctuation. Normalize this field by:
   - Converting all text to lowercase.
   - Replacing all non-alphanumeric characters (anything not `a-z`, `0-9`) with a single space.
   - Collapsing multiple consecutive spaces into a single space, and trimming leading/trailing spaces.
4. **Rolling Statistics & Anomaly Detection**: After deduplicating, sorting, and imputing, compute a rolling average of the *previous 3* imputed sensor values. 
   - If fewer than 3 previous values exist, the anomaly flag is `0`.
   - If the *current imputed value* is strictly greater than the rolling average of the previous 3 values by more than `15.0`, flag it as an anomaly (`1`). Otherwise, the flag is `0`.

Save your final output to `/home/user/clean_alerts.csv`. 
The output must include a header: `timestamp,imputed_value,normalized_desc,is_anomaly`.
Values should be printed exactly as computed (do not enforce a specific number of decimal places for the output).

Example expected output row:
`1005,95.5,warning overheat,1`