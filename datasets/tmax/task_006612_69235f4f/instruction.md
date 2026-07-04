You are acting as a compliance officer auditing a multi-system transaction environment. Recently, the system experienced severe transaction lockups. You need to identify deadlocked transactions, determine their relative financial priority, and list the resources they were holding to compile an audit report.

You are given three data sources representing different parts of the system:
1. **Relational Data (SQLite):** `/home/user/tx_history.db`
   Contains a table `transactions (tx_id INTEGER, user_id INTEGER, amount REAL, timestamp TEXT)`.
2. **Document Data (JSON Lines):** `/home/user/lock_events.jsonl`
   Contains execution logs. Each line is a JSON object with keys: `tx_id`, `event` (e.g., "acquire", "release", "wait"), and `resource` (the name of the resource).
3. **Graph Data (CSV):** `/home/user/wait_graph.csv`
   Contains the wait-for graph of transactions. It has no header. The format is `waiting_tx_id,holding_tx_id` (meaning the first transaction is waiting for a lock held by the second transaction).

**Your Task:**
1. **Detect Deadlocks:** Identify all transactions involved in a *direct 2-node deadlock cycle*. A direct cycle occurs when Transaction A is waiting on Transaction B, and Transaction B is simultaneously waiting on Transaction A. (Do not worry about 3+ node cycles).
2. **Analyze Relative Priority:** For *only* the transactions identified in step 1, query the SQLite database to determine their `amount_rank`. The `amount_rank` is defined as the rank of the transaction's `amount` compared to *all* other transactions belonging to the *same* `user_id`. The highest amount for a user gets rank 1. Use standard SQL window functions (e.g., `RANK()`).
3. **Extract Held Resources:** For the deadlocked transactions, extract the list of unique `resource`s they successfully acquired (where `event` equals `"acquire"`) from the JSONL file.
4. **Compile and Export:** Combine these insights into a single formatted JSON array and save it to `/home/user/deadlock_audit.json`.

**Output Format Specification:**
The file `/home/user/deadlock_audit.json` must contain a single JSON array of objects, sorted by `tx_id` in ascending order. Each object must strictly follow this structure:
```json
[
  {
    "tx_id": 101,
    "user_id": 5,
    "amount_rank": 2,
    "resources_held": ["RESOURCE_A", "RESOURCE_B"]
  }
]
```
Note: `resources_held` must be a JSON array of strings, sorted alphabetically. If a transaction acquired no resources, it should be an empty array `[]`.

Use standard CLI tools (`sqlite3`, `jq`, `awk`, `bash`, etc.) to process and correlate the data.