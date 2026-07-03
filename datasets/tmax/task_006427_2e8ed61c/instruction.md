You are acting as a technical assistant for a compliance officer auditing a financial platform's systems. 

We suspect there is a cyclic funds transfer ring (which recently caused a database deadlock during concurrent transaction processing) hiding in our system logs. 

An SQLite database is located at `/home/user/audit.db`. It contains a single table named `transfers` with the following schema:
- `tx_id` (INTEGER PRIMARY KEY)
- `sender_id` (INTEGER)
- `receiver_id` (INTEGER)
- `timestamp` (DATETIME)
- `amount` (DECIMAL)

Your task is to write and execute a Bash script that queries this database to identify a specific cyclic transfer ring. 
A "cyclic transfer ring" of length 3 occurs when:
1. Account A transfers money to Account B.
2. Account B transfers money to Account C.
3. Account C transfers money back to Account A.

Write a bash script at `/home/user/find_ring.sh` that extracts the `tx_id`s of the three transactions forming this cycle. 

The script must:
1. Query the SQLite database for the cycle of length 3. You can assume there is exactly one such discrete cycle in the database.
2. Output the three `tx_id`s as a comma-separated list, sorted in numerical (ascending) order.
3. Save this comma-separated string to exactly `/home/user/deadlock_cycle.txt` (no trailing newline is required, but a single trailing newline is acceptable).

Ensure your script operates entirely via Bash and `sqlite3` CLI commands.