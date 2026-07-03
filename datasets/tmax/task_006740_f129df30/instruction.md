You are a Database Reliability Engineer (DBRE) tasked with analyzing backup metadata across several database clusters. 

The backup metadata is stored in an SQLite database located at `/home/user/backup_catalog.db`. 

The database has two tables:
1. `clusters`
   - `id` (INTEGER PRIMARY KEY)
   - `name` (TEXT)
   - `region` (TEXT)
2. `backups`
   - `id` (INTEGER PRIMARY KEY)
   - `cluster_id` (INTEGER, foreign key to clusters.id)
   - `timestamp` (TEXT, ISO 8601 format)
   - `size_bytes` (INTEGER)
   - `status` (TEXT, either 'SUCCESS' or 'FAILED')

Your task is to write a Python script at `/home/user/analyze_backups.py` that generates a JSON report of the backups for a specific region. 

The script must meet the following requirements:
1. It must accept a `--region` command-line argument (e.g., `python3 analyze_backups.py --region us-east-1`).
2. It must use parameterized queries (e.g., `?` placeholders) when querying the database by region or status to prevent SQL injection.
3. For the specified region, find the latest successful backup for each cluster. To demonstrate pagination, you must retrieve the `backups` table rows in batches of 5 (using `LIMIT 5` and `OFFSET`) sorted by `timestamp` DESC. Filter these paginated results in your Python code or query to process only 'SUCCESS' backups.
4. Use a separate aggregated query (with `GROUP BY`) to calculate the total size of all successful backups ever recorded for each cluster in the given region.
5. Combine the data and output a strictly formatted JSON file at `/home/user/backup_report.json`.

The expected JSON format for `/home/user/backup_report.json` is:
```json
{
  "region": "<REGION_NAME>",
  "clusters": {
    "<cluster_name>": {
      "latest_backup_id": <id_of_latest_successful_backup>,
      "latest_backup_timestamp": "<timestamp_of_latest_successful_backup>",
      "total_successful_size_bytes": <sum_of_all_success_sizes>
    }
  }
}
```
If a cluster has no successful backups, omit it from the `clusters` object.

To complete the task, execute your script for the region `us-west-2` so the final `/home/user/backup_report.json` is generated for verification.