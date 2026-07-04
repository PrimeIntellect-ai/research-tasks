You are acting as a Database Reliability Engineer (DBRE) investigating a recent spike in backup job failures across our NoSQL clusters. 

System logs of our NoSQL backup agent have been dumped to a JSON Lines file at `/home/user/backup_logs.jsonl`. Each line represents a backup job document with the following schema:
`{"job_id": "string", "cluster": "string", "status": "string", "duration_seconds": int, "timestamp": "string"}`

Your task is to write a Python script at `/home/user/process_backups.py` that mimics a NoSQL aggregation pipeline to process this data, filter and sort it, and export a summarized report. 

The Python script must perform the following operations:
1. **Filter**: Keep only the documents where `"status"` is exactly `"FAILED"`.
2. **Aggregate/Group**: Group the filtered records by the `"cluster"` field.
3. **Calculate & Sort**: For each cluster, calculate the average `duration_seconds` of all its failed jobs (rounded to 1 decimal place).
4. **Paginate/Limit**: Identify the top 3 longest failing jobs for each cluster. Sort by `duration_seconds` in descending order. If there is a tie in duration, resolve it by sorting `job_id` in ascending alphabetical order.
5. **Export**: Write the results to a CSV file at `/home/user/failed_backups_report.csv`. 

The CSV file must have exactly the following header line:
`cluster,avg_failed_duration,longest_job_1,longest_job_2,longest_job_3`

For the rows:
- Sort the rows alphabetically by the `cluster` name in ascending order.
- `avg_failed_duration` should be formatted to 1 decimal place (e.g., `125.0`).
- `longest_job_1` to `longest_job_3` should contain the `job_id` of the top 3 longest jobs. If a cluster has fewer than 3 failed jobs, leave the remaining columns empty (e.g., `ClusterX,150.0,job123,,`).
- Clusters with no failed jobs should not be included in the output.

Run your script to produce the output file. The automated test will verify the contents of `/home/user/failed_backups_report.csv`.