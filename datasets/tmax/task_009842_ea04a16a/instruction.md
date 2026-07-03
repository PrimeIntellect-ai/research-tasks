You are a DevOps engineer debugging a log processing pipeline. 

A Bash script `/home/user/process.sh` is designed to read container logs from `/home/user/app_logs/`, decode a Base64-encoded JSON payload from each log line, extract a `sensor_reading` floating-point value using `jq`, and compute the total sum of all readings.

However, the script has two issues:
1. **Intermittent Failure / Encoding Troubleshooting:** The script crashes and aborts intermittently during the pipeline execution. A specific edge-case log entry contains improperly serialized, non-UTF-8 bytes within the payload string, which causes `jq` to panic and the pipeline to fail.
2. **Precision Loss:** The final sum calculated by the script is losing floating-point precision due to how the aggregation is currently written.

Your task:
1. Identify the log entry causing the crash.
2. Modify `/home/user/process.sh` to gracefully handle or clean the corrupted encoding (stripping out invalid UTF-8 characters) before parsing so that `jq` successfully processes the valid JSON structure and extracts the `sensor_reading`. Do not drop the entire log line.
3. Fix the precision loss issue in the final sum calculation inside the script. The final sum must be formatted to exactly 8 decimal places.
4. Run your fixed script. It should write the precise final sum to `/home/user/total_sum.txt`.

Ensure your modifications are robust and that the final output file `/home/user/total_sum.txt` contains only the accurate total sum.