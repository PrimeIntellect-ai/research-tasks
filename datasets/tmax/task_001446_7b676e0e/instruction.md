You are a log analyst investigating a data quality issue in an ETL pipeline. Downstream consumers are reporting duplicate records, and we suspect it is related to the pipeline's retry mechanism.

You have been provided with two files in the `/home/user/data` directory:
1. `/home/user/data/pipeline_logs.jsonl`: A JSON Lines file containing the execution logs of the ETL jobs. Each line is a JSON object with keys: `timestamp`, `job_id`, `status` (can be "STARTED", "FAILED", "RETRYING", "SUCCESS"), and `records_processed`.
2. `/home/user/data/output_data.csv`: The actual output produced by these jobs. It has the headers: `record_id`, `job_id`, `data_payload`.

The hypothesis is that when a job fails and is retried, the ETL framework does not clean up the records written during the initial failed attempt. This causes duplicate `record_id`s to be present in the CSV for that specific `job_id`.

Your task is to write a Python script at `/home/user/analyze_retries.py` that processes these files and generates an anomaly report. The script must:
1. Parse the JSONL logs to identify all `job_id`s that experienced at least one "RETRYING" status.
2. Read the CSV file and calculate how many *duplicate* `record_id`s exist specifically for those retried jobs. (If a `record_id` appears 2 times for a job, that is 1 duplicate. If it appears 3 times, that is 2 duplicates).
3. Identify which retried job produced the highest number of duplicates.
4. Output the results to `/home/user/anomaly_report.json` in the exact following format:

```json
{
    "retried_jobs": ["<job_id_1>", "<job_id_2>"],
    "total_duplicates_from_retries": <integer>,
    "max_retry_spike_job": "<job_id_with_most_duplicates>"
}
```
*Note: The `retried_jobs` array should be sorted alphabetically.*

Once you have written and executed your script to generate `/home/user/anomaly_report.json`, your task is complete.