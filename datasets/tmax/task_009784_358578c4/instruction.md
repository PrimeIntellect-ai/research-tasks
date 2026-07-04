You are tasked with building a Bash-based data processing pipeline to analyze configuration manager logs. 

You have a set of raw JSON-lines (.jsonl) log files located in `/home/user/raw_logs/`. Each file corresponds to a different server (e.g., `server_alpha.jsonl`, `server_beta.jsonl`). These logs track the number of configuration mutations applied over time.

However, the logging agent had a bug: some log lines contain invalid, unescaped literal unicode sequences like `\uZZZZ` which break standard parsers. 

Write a Bash script at `/home/user/analyze_logs.sh` that performs the following steps:

1. **Parallel Processing**: The script must process all `.jsonl` files in `/home/user/raw_logs/` in parallel (e.g., using background jobs `&` or `xargs -P`).
2. **Sanitization**: For each file, filter out any line containing the literal string `\uZZZZ` before parsing.
3. **Data Extraction**: For valid lines, extract the `ts` (Unix timestamp, integer) and `mutations` (integer) fields.
4. **Aggregation & Imputation**: 
   - Group the data by "hour index", defined as the integer division of the timestamp by 3600 (`hour_index = ts / 3600`).
   - Sum the `mutations` for each hour index.
   - The time series must be continuous. Determine the minimum and maximum hour index for each file. For any hour index between the min and max (inclusive) that has no valid log entries, impute the hourly mutations as `0`.
5. **Rolling Statistics**: Calculate a 3-hour rolling sum of mutations. For any given `hour_index`, this is the sum of mutations in `hour_index`, `hour_index - 1`, and `hour_index - 2`.
6. **Output**: Write the results for each input file to `/home/user/processed/<filename>.csv` (e.g., `server_alpha.csv`). 
   - The CSV should have no header.
   - Format: `hour_index,hourly_mutations,rolling_3h_sum`
   - Sort the output sequentially by `hour_index` in ascending order.

Ensure your script is executable (`chmod +x /home/user/analyze_logs.sh`) and uses only standard Linux CLI tools (Bash built-ins, `awk`, `sed`, `grep`, `jq`, `xargs`, etc.). 
Do not use Python, Perl, or other scripting languages.

Execute your script to produce the output files. We will verify the contents of `/home/user/processed/*.csv`.