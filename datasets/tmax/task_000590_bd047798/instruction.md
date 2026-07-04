You are a data engineer responsible for fixing a broken ETL pipeline that processes time-series IoT sensor data. 

We receive a CSV file at `/home/user/raw_sensor_data.csv`. The naive pipeline fails because some sensor descriptions contain embedded newlines inside quoted fields, causing rows to be silently dropped or mangled by traditional line-by-line tools.

Your task is to write a single Bash script at `/home/user/etl_pipeline.sh` (using standard Unix tools like `awk`, `sed`, `sort`, `md5sum`, `jq`, etc.) that performs the following ETL steps:

1. **Clean Embedded Newlines (Regex/Parsing):** Parse the CSV and replace any embedded newlines *within quoted fields* with a single space ` `. Ensure all rows stay intact.
2. **Hash-Based Deduplication:** Duplicate readings are sometimes transmitted. Compute the MD5 hash of the concatenated string `<timestamp><sensor_id>` for each row. Only keep the *first* occurrence of each hash. Keep the CSV header.
3. **Normalization:** Find the global minimum and maximum values of the `value` column across the entire dataset. Append a new column called `norm_value` to the CSV, which is the Min-Max scaled value: `(value - min) / (max - min)`. Format this value to exactly 4 decimal places.
4. **Distance & Anomaly Detection:** For each sensor independently, sort the readings by `timestamp` chronologically. Calculate the absolute difference between the `norm_value` of the current reading and the immediate previous reading for that same sensor. 
    * If this distance is strictly greater than `0.5`, log it as an anomaly.
5. **Output Formatting:**
    * Save the fully cleaned, deduplicated, and normalized dataset to `/home/user/cleaned_data.csv`. (Columns: `timestamp,sensor_id,value,notes,norm_value`)
    * Save the anomalies to `/home/user/anomalies.csv`. (Columns: `timestamp,sensor_id,distance`). The distance should be printed to 4 decimal places. Sort the anomalies chronologically by timestamp.

**Constraints:**
* Use Bash as the primary execution engine. You may use inline `awk`, `sed`, `perl`, `python`, etc., if called directly from within your `etl_pipeline.sh` script.
* Do not use external libraries that require `pip install` or internet access; rely on standard pre-installed Linux utilities.
* The script must execute automatically when run via `bash /home/user/etl_pipeline.sh`.