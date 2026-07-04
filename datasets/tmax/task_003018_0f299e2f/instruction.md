You are a Database Reliability Engineer (DBRE) investigating a backup anomaly. Last night, a severe database deadlock occurred during the backup window. The backup system pulls data from three different datastores (Relational, Document, and Graph) into a unified backup directory. You suspect the deadlock caused a partial transaction failure, leading to inconsistencies across the representations. 

You have been provided with the following files in `/home/user/backup/`:
1. `relational.db`: A SQLite database containing `users` (id, name) and `transactions` (tx_id, user_id, amount, status, created_at).
2. `documents.json`: A JSON file containing user metadata arrays. Each document should adhere to this schema:
   - `user_id`: Integer (Required)
   - `preferences`: Dictionary (Required)
   - `last_tx_id`: String (Required, format: 'tx' followed by numbers, e.g., 'tx101')
3. `graph.csv`: A CSV edge list representing financial transfers (`sender_id`, `receiver_id`, `tx_id`).

Your task is to write a Python script `/home/user/audit_backup.py` that performs cross-representation mapping and output schema validation to find anomalies. Running your script must generate a report at `/home/user/anomalies.json` with the following exact JSON structure:
```json
{
  "missing_tx_ids": ["<tx_id_1>", "<tx_id_2>"],
  "invalid_doc_user_ids": [<user_id_1>, <user_id_2>]
}
```
Rules for anomalies:
- `missing_tx_ids`: Any `tx_id` that appears in `documents.json` (as `last_tx_id`) OR in `graph.csv` (as `tx_id`), but is missing from the `transactions` table in `relational.db`. Sort this list alphabetically.
- `invalid_doc_user_ids`: The `user_id` of any document in `documents.json` that violates the required schema described above (missing keys, wrong types, or malformed `last_tx_id`). Sort this list in ascending order.

Finally, you discovered the deadlock was caused by concurrent updates contending with a slow read query: 
`SELECT * FROM transactions WHERE user_id = ? AND status = 'PENDING' ORDER BY created_at DESC;`

Design an optimal index strategy to speed up this exact query and avoid full table scans. Write the `CREATE INDEX` statement into a file named `/home/user/index_strategy.sql`. Name the index `idx_tx_user_status_created`.