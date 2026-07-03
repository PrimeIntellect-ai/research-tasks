You are a log analyst investigating traffic patterns for a new web application. 

You have been provided with a JSON-formatted access log located at `/home/user/app_access.log`. Each line in the file is a valid JSON object representing a single HTTP request, containing the following fields: `timestamp` (ISO 8601 format, e.g., "2023-10-25T14:32:05Z"), `ip` (client IP address), `status` (HTTP status code), and `bytes` (size of the response in bytes).

Your task is to perform a windowed aggregation to summarize the traffic on a per-minute basis. 

You must extract the relevant features and compute the following summary statistics for each 1-minute tumbling window:
1. `total_bytes`: The sum of the `bytes` field for all requests in that minute.
2. `distinct_ips`: The count of unique `ip` addresses that made requests in that minute.
3. `max_bytes`: The maximum value of the `bytes` field among requests in that minute.

Create a CSV file at `/home/user/minute_stats.csv` with the results. 
The CSV must have the following exact header:
`window,total_bytes,distinct_ips,max_bytes`

The `window` column should represent the minute of the aggregation in the format `YYYY-MM-DDTHH:MM` (e.g., `2023-10-25T14:32`).
The rows in the CSV must be sorted chronologically by the `window` column. Ensure there are no spaces after commas.

You can use any standard command-line tools (like `jq`, `awk`, `sort`) or write a quick script in Python, Bash, or another available language to process the data.