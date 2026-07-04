You are a log analyst dealing with a corrupted application log file. You have been tasked with building a robust data processing pipeline in Bash to clean, transform, and sample these logs.

The input file is located at `/home/user/raw_logs.jsonl`. It is a JSON-lines file containing web requests, but it cannot be parsed by standard tools like `jq` because a bug in the logging library injected malformed Unicode escape sequences (e.g., invalid hex characters like `\u002Z` or truncated escapes like `\u12`) into the `user_agent` field.

You need to write a Bash script at `/home/user/process_logs.sh` that performs the following steps:

1. **Data Cleaning**: Pre-process the lines to remove any malformed Unicode escape sequences (anything matching `\u` followed by characters that do not form a valid 4-digit hex code) so that the file becomes valid JSON.
2. **Parallel Processing**: Process the cleaned lines in parallel using `xargs -P` or `GNU parallel` to speed up execution.
3. **Feature Extraction & Timestamp Alignment**: Extract the `timestamp`, `ip_address`, `status`, and `user_agent` fields. The `timestamp` field in the raw logs mixes Unix epoch timestamps (integers) and custom formats (e.g., `DD/MMM/YYYY:HH:MM:SS`). Convert all timestamps to strict ISO 8601 format (`YYYY-MM-DDTHH:MM:SSZ` in UTC).
4. **Data Masking (Anonymization)**: Mask the IPv4 addresses in the `ip_address` field by changing the last octet to `0` (e.g., `192.168.12.34` becomes `192.168.12.0`). 
5. **Data Sampling and Stratification**: After transforming the data, collect the results and perform stratified sampling. Select exactly 3 random log entries for each unique HTTP `status` code present in the dataset.

Your final output must be written to `/home/user/stratified_sample.jsonl`.
- The output must be valid JSON-lines.
- Each line must contain exactly these keys: `timestamp`, `ip_address`, `status`, and `user_agent`.
- The file must contain exactly 3 lines per HTTP status code found in the original logs. 

Ensure your script `/home/user/process_logs.sh` is executable and run it to generate the final output. You may install standard command-line tools like `jq`, `parallel`, or `gawk` if they are not already present.