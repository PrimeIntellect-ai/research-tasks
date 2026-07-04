You are a Database Administrator working with a large export of application metrics from a NoSQL database. The database lacks proper indexing and window function capabilities for ad-hoc analytical queries, so you frequently use Bash command-line tools to simulate NoSQL aggregation pipelines and analytical aggregations.

A daily export is located at `/home/user/metrics.jsonl`. It contains Newline Delimited JSON (NDJSON) records with the following schema:
`{"host": "string", "process": "string", "memory_mb": float}`

Your task is to write a highly efficient Bash script at `/home/user/optimize.sh` that simulates a windowed aggregation pipeline. The script must:
1. Read `/home/user/metrics.jsonl`.
2. Extract the data and logically partition it by `host`.
3. Order the partitions by `memory_mb` in descending order.
4. Select only the top 1 process (the one consuming the most memory) for each `host`.
5. Output the results to `/home/user/top_metrics.csv` in standard CSV format: `host,process,memory_mb`.
6. The final CSV must be sorted alphabetically by `host`.

To ensure your script is performant and mimics efficient index scanning, you must stream the data using a combination of `jq`, `sort`, and `awk` (or similar coreutils). Do not slurp the entire JSON file into memory at once with `jq -s`. 

Ensure `/home/user/optimize.sh` is executable and cleanly produces the `/home/user/top_metrics.csv` file upon execution.