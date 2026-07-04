You are acting as a compliance officer auditing an organization's internal systems for unauthorized access. 

You have been provided with two data sources:
1. A relational SQLite database at `/home/user/employees.db`. It contains two tables:
   - `users` (schema: `id INTEGER PRIMARY KEY, name TEXT, role TEXT`)
   - `permissions` (schema: `role TEXT, resource TEXT`)
2. A document-based access log in JSON Lines format at `/home/user/access_logs.jsonl`. Each line represents a system access event and contains the following keys: `timestamp`, `user_id`, and `resource`.

Your objective is to map the document-based log entries against the relational role-based access control (RBAC) database to identify any unauthorized access events (i.e., when a user accesses a resource that is not explicitly granted to their role in the `permissions` table).

Task requirements:
1. Write a Python script to cross-reference the JSONL logs with the SQLite database.
2. You must use parameterized SQLite queries in Python to securely look up user roles and permissions based on the log entries.
3. Chaining the results of this mapping, export all identified compliance violations to a CSV file located at `/home/user/violations.csv`.
4. The output CSV must have exactly the following header: `timestamp,user_id,name,role,resource`.
5. The CSV should contain only the violation events, sorted chronologically by `timestamp` in ascending order.
6. Ensure your script handles the data retrieval and mapping efficiently.

Create the required CSV file at `/home/user/violations.csv` to complete the audit.