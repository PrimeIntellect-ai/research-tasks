You are a Database Reliability Engineer (DBRE) tasked with recovering critical financial data from a potentially corrupted SQLite backup file. 

The backup file is located at `/home/user/legacy_backup.db`. A recent storage failure caused some SQLite indices in this file to become corrupted, returning stale or missing rows when queried normally. However, the underlying table data pages are intact.

Your goal is to write a Python script `/home/user/recover_data.py` that performs a safe extraction and aggregation of data, bypassing any corrupted indices.

Here are your instructions:
1. Reverse engineer the data model in `/home/user/legacy_backup.db` to identify all tables that start with the prefix `sales_` (these are regional shard tables).
2. Read a list of target user IDs from `/home/user/target_users.json`.
3. For each target user, dynamically construct parameterized queries to calculate the total `amount` and the total number of transactions across ALL `sales_` tables where the `status` is exactly `'COMPLETED'`.
4. CRITICAL: Because the indices are corrupted, your queries MUST force SQLite to perform a full table scan by using the `NOT INDEXED` clause for every `sales_` table you query.
5. Aggregate the results across all shards for each user.
6. Export the final aggregated data to `/home/user/recovery_report.json`.

The output file `/home/user/recovery_report.json` must strictly follow this JSON schema:
- A root JSON object where keys are the `user_id` (as strings).
- Values are objects containing:
  - `total_amount` (float): The sum of all completed transaction amounts for that user across all shards.
  - `transaction_count` (int): The total number of completed transactions for that user across all shards.

Example expected format for `/home/user/recovery_report.json`:
```json
{
  "101": {
    "total_amount": 150.50,
    "transaction_count": 2
  },
  "204": {
    "total_amount": 0.0,
    "transaction_count": 0
  }
}
```

Ensure your Python script is executed and successfully generates the output file before completing the task.