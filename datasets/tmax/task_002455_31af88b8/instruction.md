You are a Database Reliability Engineer (DBRE) investigating a potential storage issue with your NoSQL database backups. 

You have been provided with a JSONL (JSON Lines) file containing NoSQL-style backup metadata at `/home/user/backup_data.jsonl`. Each line represents a backup event document with nested metrics.

Your task is to identify "anomalous" collections whose most recent successful backup size has spiked significantly. 

Write a Python script (e.g., `/home/user/analyze.py`) that performs the following NoSQL aggregation pipeline logic:
1. Parse the JSON documents.
2. Filter out any backups where `metrics.status` is NOT `"success"`.
3. For each `collection`, calculate the moving average of `metrics.size_bytes` over its **last 3 successful backups** (ordered by `timestamp` ascending). If a collection has fewer than 3 successful backups, calculate the average over however many successful backups it has. Note: The most recent backup is included in this 3-backup window.
4. Identify collections where the `metrics.size_bytes` of the **most recent** successful backup is strictly greater than **1.5 times** the calculated average of its last 3 successful backups.
5. Write the names of these anomalous collections to `/home/user/anomalies.txt`, one collection name per line, sorted alphabetically.

Example document format:
`{"backup_id": "b1", "collection": "users", "timestamp": "2023-10-01T10:00:00Z", "metrics": {"size_bytes": 1000, "duration": 10, "status": "success"}}`

Ensure you output the exact `/home/user/anomalies.txt` file as specified to complete the task.