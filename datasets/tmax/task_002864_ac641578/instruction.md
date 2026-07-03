You are assisting a compliance officer auditing an internal system for transaction anomalies. As part of this audit, you need to identify deadlocks that occurred between concurrent transactions in the system's history. 

An SQLite database containing the audit logs is located at `/home/user/audit_logs.db`. 
The database contains two tables: `transactions` and `lock_requests`. You will need to inspect the schema of this database to understand the relationships.

Your task is to write a C program at `/home/user/detect_deadlocks.c` and compile it to `/home/user/detect_deadlocks`. When executed, this program must:
1. Connect to `/home/user/audit_logs.db`.
2. Analyze the wait-for relationships between transactions. A transaction T1 is "waiting for" T2 if T1 has a 'WAITING' lock request for a resource that T2 currently holds (indicated by a 'GRANTED' lock request for that same resource).
3. Filter the transactions to only consider those whose `start_time` is strictly after `2023-01-01 00:00:00`. BOTH transactions in a wait-for relationship must meet this time criteria to be considered.
4. Detect simple deadlocks of length 2 (i.e., T1 is waiting for T2, AND T2 is waiting for T1).
5. Output the detected deadlocks into a file named `/home/user/deadlocks.json`.

The output must be strictly valid JSON that matches the following schema:
```json
{
  "deadlocks": [
    {"tx1": <smaller_tx_id>, "tx2": <larger_tx_id>}
  ]
}
```
The `deadlocks` array must be sorted by `tx1` in ascending order, and then by `tx2` in ascending order. Each pair must only be listed once, ensuring `tx1` < `tx2`.

Constraints & Guidelines:
- You must write the solution primarily in C, utilizing the SQLite3 C API (`sqlite3.h`). 
- You may use standard shell commands to compile your code (e.g., `gcc /home/user/detect_deadlocks.c -o /home/user/detect_deadlocks -lsqlite3`) and explore the database.
- Do not make any modifications to the `/home/user/audit_logs.db` database.