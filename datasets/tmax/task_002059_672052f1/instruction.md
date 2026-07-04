You are a log analyst investigating traffic patterns across a distributed application. The application logs are stored in multiple files, and you need to process them to create an aggregated, anonymized time-series report that can be shared externally.

The logs are located in `/home/user/logs/` and are named `node_1.log`, `node_2.log`, `node_3.log`, and `node_4.log`.

Each log file has the following format (space-separated):
`[TIMESTAMP] IP_ADDRESS HTTP_METHOD PATH HTTP_STATUS`
Example:
`[2023-11-15T08:34:12Z] 192.168.12.45 GET /Api/v1/Users?id=5 200`

Your goal is to write and execute a Bash script `/home/user/process_logs.sh` that processes these logs and generates a single CSV report at `/home/user/final_report.csv`.

Your pipeline must adhere to the following rules:
1. **Time-based bucketing:** Round each timestamp down to the nearest 10-minute boundary. For example, `2023-11-15T08:34:12Z` becomes `2023-11-15T08:30:00Z`.
2. **Data masking:** Anonymize the IPv4 address by replacing the last octet with `000`. For example, `192.168.12.45` becomes `192.168.12.000`.
3. **Normalization:** Extract the PATH. Convert it to lowercase and completely remove any query string parameters (everything from the `?` character onward). For example, `/Api/v1/Users?id=5` becomes `/api/v1/users`.
4. **Parallel processing:** Your script must process the multiple log files in parallel. You can use standard bash job control (`&` and `wait`), `xargs -P`, or `parallel` to achieve this. Each file should be processed into an intermediate state before being merged.
5. **Aggregation:** Count the number of requests for each unique combination of `(Bucket, Masked_IP, Normalized_Path)`.
6. **Output:** The final output must be saved to `/home/user/final_report.csv`. It should be a comma-separated file with the header `Timestamp,IP,Path,Count`. The rows must be sorted chronologically by Timestamp, then alphabetically by IP, and then alphabetically by Path.

Write the script, ensure it has executable permissions, and run it to produce the final CSV. You only have access to Bash built-ins and standard POSIX/Linux CLI tools (e.g., awk, sed, grep, sort, uniq, xargs).