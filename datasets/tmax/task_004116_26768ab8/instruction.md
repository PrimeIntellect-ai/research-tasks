You are a data scientist cleaning a time-series dataset of server metrics before it can be shared with external analysts. You have a raw CSV dump located at `/home/user/raw_metrics.csv`. 

The raw CSV has the following header and format:
`timestamp,user_id,ip_address,cpu_usage`
Example row: `2023-10-12T14:35:22Z,U9482,192.168.1.45,84.5`

Using only standard Linux command-line tools (like `awk`, `sed`, `grep`, `bash`), create a data processing pipeline that reads this file and generates a cleaned dataset at `/home/user/clean_metrics.csv` satisfying the following requirements:

1. **Feature Extraction:** Split the `timestamp` into two separate columns: `date` (YYYY-MM-DD) and `hour` (HH, zero-padded).
2. **Data Masking (Anonymization):** Mask the `ip_address` by replacing its final octet (the numbers after the last dot) with `XXX` (e.g., `192.168.1.45` becomes `192.168.1.XXX`).
3. **Feature Transformation:** Create a new column called `usage_category`. If `cpu_usage` is greater than or equal to `80.0`, the value should be `HIGH`. Otherwise, it should be `NORMAL`.
4. **Output Format:** The new file must be a comma-separated CSV with the following exact header:
   `date,hour,user_id,masked_ip,cpu_usage,usage_category`
5. **Pipeline Logging:** After the processing is complete, count the number of data rows processed (excluding the header) and write exactly the following string to `/home/user/pipeline.log`:
   `Processed <N> rows.` (where `<N>` is the number of data rows).

Ensure your solution handles the header row correctly and processes all data rows accurately. Do not use external scripting languages like Python or Perl; stick to shell built-ins and standard POSIX utilities (awk, sed, etc.).