You are acting as a systems compliance officer auditing financial records. You have been tasked with identifying suspicious transaction patterns indicative of account takeover or compliance breaches.

A local SQLite database exists at `/home/user/compliance.db`. It contains three tables:

1. `users`
   - `user_id` (INTEGER PRIMARY KEY)
   - `country_code` (TEXT) - The user's registered country code (e.g., 'US', 'UK')

2. `transactions`
   - `tx_id` (TEXT PRIMARY KEY)
   - `user_id` (INTEGER)
   - `amount` (REAL)
   - `tx_timestamp` (DATETIME) - Format: YYYY-MM-DD HH:MM:SS

3. `access_logs`
   - `log_id` (INTEGER PRIMARY KEY)
   - `user_id` (INTEGER)
   - `ip_address` (TEXT)
   - `ip_country` (TEXT) - Geocoded country of the IP
   - `log_timestamp` (DATETIME) - Format: YYYY-MM-DD HH:MM:SS

Your task is to:
1. Write a SQL script at `/home/user/index.sql` containing the `CREATE INDEX` statements necessary to optimize the search described below. You must design an index strategy that targets the `access_logs` table to optimize filtering by `user_id` and time bounds.
2. Write a C++ program at `/home/user/audit.cpp` that connects to `/home/user/compliance.db` using the SQLite3 C/C++ API.
3. Your C++ program must execute a complex query (utilizing joins, subqueries, and SQLite's built-in JSON aggregation functions to simulate NoSQL document generation) that finds all transactions meeting ALL of these criteria:
   - The transaction `amount` is strictly greater than 10000.
   - The user had an `access_log` entry where the `ip_country` does NOT match the user's registered `country_code`.
   - The suspicious `access_log` entry occurred within 24 hours (before or after) of the `tx_timestamp`.
4. The query must use SQLite's JSON functions (e.g., `json_group_array`, `json_object`) to format the output schema directly in the database engine.
5. The C++ program must write the exact resulting JSON string to `/home/user/audit_results.json`. The JSON should be an array of objects, with each object strictly adhering to this schema:
   `[{"tx_id": "<string>", "user_id": <int>, "amount": <float>, "flagged_ip": "<string>"}]`
   (If multiple logs match for a single transaction, pick the one with the most recent `log_timestamp`).

Requirements:
- You must compile your C++ program to `/home/user/audit_runner`. 
- `libsqlite3-dev` is already installed, compile with `g++ -O2 /home/user/audit.cpp -o /home/user/audit_runner -lsqlite3`.
- Execute `./audit_runner` to generate the output file.
- Apply your index optimization script to the database via `sqlite3 /home/user/compliance.db < /home/user/index.sql` before running the C++ program to ensure optimal execution.