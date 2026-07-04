You are a data engineer tasked with fixing and analyzing a broken ETL pipeline. An upstream job failed and was retried, resulting in a dataset filled with duplicate records. Furthermore, the downstream team suspects there are anomalies in the deduplicated sensor readings.

You need to build a Bash-only pipeline to clean the data, calculate rolling statistics, and detect anomalies. 

The raw data is located at `/home/user/raw_data.csv` with the header:
`timestamp,sensor_id,value`

Your task is to write a master pipeline script at `/home/user/run_pipeline.sh` that executes the following steps using only Bash built-ins, coreutils, and standard tools like `awk`, `sed`, `sort`, etc. (Do not use Python, Perl, or Node.js).

**Phase 1: Hash-based Deduplication**
Create a deduplicated version of the dataset at `/home/user/deduped.csv`. 
1. For every row (excluding the header), compute the MD5 hash of the entire row's text.
2. Deduplicate the rows based on this hash, keeping only the *first* occurrence of each hash.
3. The output file `/home/user/deduped.csv` must include a new header `hash,timestamp,sensor_id,value`.
4. The data rows should contain the computed MD5 hash followed by the original columns.

**Phase 2: Rolling Statistics & Anomaly Detection**
Process `/home/user/deduped.csv` to find anomalous readings. 
1. For each `sensor_id`, maintain a rolling average of the `value` of the **last 3** readings (strictly prior to the current reading). If there are fewer than 3 previous readings for a sensor, use the available previous readings to calculate the average. If it is the first reading for a sensor, the rolling average is `0`.
2. A reading is flagged as an anomaly if its `value` is strictly greater than `2.0 * rolling_average` AND the sensor has at least 1 prior reading.
3. Output the anomalies to `/home/user/anomalies.csv` with the header: `timestamp,sensor_id,value,rolling_avg`.
4. Format the `rolling_avg` to 2 decimal places. 
5. The output should maintain the chronological order (the order they appear in the deduplicated file).

**Requirements:**
- Make sure `/home/user/run_pipeline.sh` is executable and runs seamlessly without arguments.
- The pipeline should overwrite `/home/user/deduped.csv` and `/home/user/anomalies.csv` upon successive runs.