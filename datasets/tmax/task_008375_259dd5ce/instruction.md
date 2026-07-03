You are assisting a Compliance Officer in auditing system access logs to detect unauthorized privilege escalations. 

We have a centralized SQLite database located at `/home/user/corporate.db` that stores employee data and a unified application event log. The event logs are stored as JSON documents within a relational column, mimicking a NoSQL document store.

The database contains the following tables:
1. `users` (id INTEGER PRIMARY KEY, name TEXT, dept_id INTEGER)
2. `roles` (user_id INTEGER PRIMARY KEY, role TEXT, clearance INTEGER)
3. `events` (event_id INTEGER PRIMARY KEY, event_data TEXT)

The `event_data` column contains JSON strings with the following structure:
`{"action": "READ", "resource": "vault", "timestamp": 1680000000}`

Your task is to write a C program at `/home/user/audit.c` and compile it to `/home/user/audit`. 

When executed, your C program must perform the following:
1. **Query Optimization:** Analyze the schema and programmatically execute SQL to create an expression-based index on the `events` table to optimize querying the JSON `resource` and `action` fields. A full table scan of the JSON data is considered a compliance failure due to resource constraints.
2. **Data Aggregation and Joining:** Execute a complex SQL query that:
   - Parses the JSON `event_data` to extract `action`, `resource`, and `timestamp`.
   - Joins this extracted data with the `users` and `roles` tables.
   - Filters for compliance violations: Any event where the `resource` is exactly `"vault"`, the `action` is `"READ"`, but the user's `clearance` is strictly less than `5`.
3. **Window Functions:** Use a SQL Window Function (e.g., `ROW_NUMBER()`) within your query or CTE to isolate only the **most recent** violation timestamp for each violating user.
4. **Data Export:** Retrieve the results and export them as a standard CSV file directly to `/home/user/flagged_audits.csv`.

The output CSV `/home/user/flagged_audits.csv` must have exactly this header and be ordered by `user_id` ascending:
`user_id,name,role,violation_time`

Requirements:
- Your C code must use the standard `<sqlite3.h>` library.
- You must compile your code using standard tools (e.g., `gcc /home/user/audit.c -o /home/user/audit -lsqlite3`).
- Do not use third-party libraries other than standard C libraries and `libsqlite3`.
- After writing and compiling, run your executable so it generates `/home/user/flagged_audits.csv`.