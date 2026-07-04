You are a log analyst investigating server performance anomalies. 

You have been provided with two files:
1. `/home/user/logs.jsonl`: A JSON-lines log file containing server metrics. However, the logging agent had a bug and generated invalid unicode escape sequences in the `msg` field (e.g., `\u82`), which causes standard JSON parsers like `jq` to crash when processing the entire file.
2. `/home/user/servers.csv`: A CSV file containing server mappings in the format `server_name,region`.

Your task is to identify all geographic regions that experienced a CPU load anomaly (defined as `cpu_load > 85.0`).

Perform the following steps using standard Bash utilities (awk, sed, grep, join, sort, etc.):
1. Extract the `server` and `cpu_load` values from `/home/user/logs.jsonl`. You must handle or bypass the malformed JSON lines so that no data is lost.
2. Filter the records to only keep those where `cpu_load` is strictly greater than `85.0`.
3. Join the filtered server names with `/home/user/servers.csv` to determine their regions.
4. Output the unique region names that had a CPU load > 85.0 to `/home/user/high_load_regions.txt`.
5. The output file should contain exactly one region per line, sorted alphabetically.

Ensure your solution only relies on standard CLI tools and shell built-ins available in a minimal Linux environment.