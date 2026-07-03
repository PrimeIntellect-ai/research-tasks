As a compliance officer, you are auditing our internal systems for unauthorized data access. You have been provided with two data sources:

1. A SQLite database containing the organization's access control matrix, located at `/home/user/audit.db`.
2. A JSON file containing recent access logs from the application server, located at `/home/user/logs.json`.

The database has the following schema:
- `users(id INTEGER PRIMARY KEY, name TEXT, dept_id INTEGER)`
- `departments(id INTEGER PRIMARY KEY, name TEXT)`
- `permissions(dept_id INTEGER, resource_id INTEGER, can_read INTEGER, can_write INTEGER)`

The JSON log file contains an array of objects with the following structure:
`{"timestamp": "2023-10-01T10:00:00Z", "user_id": 1, "resource_id": 100, "action": "READ"}`
(Note: `action` can be either "READ" or "WRITE").

Your task is to identify all access events in the JSON log where the user's department did not have the required permissions for the requested resource and action. 
An access is a **violation** if:
- The action is "READ" and the department's `can_read` for that resource is `0` or there is no permission record at all.
- The action is "WRITE" and the department's `can_write` for that resource is `0` or there is no permission record at all.

You must:
1. Write a C program (e.g., `audit.c`) that connects to the SQLite database (using `sqlite3.h`).
2. Use standard Linux shell tools (like `jq`) to parse the JSON logs and pipe the flattened data into your C program to avoid writing a C JSON parser.
3. In your C program, use a complex JOIN query to cross-reference the incoming log data with the relational database to determine if the access was a violation.
4. Export the identified violations to a CSV file at `/home/user/violations.csv` with the exact header: `timestamp,user_name,department_name,resource_id,action`.

Compile your C program with `gcc -o audit audit.c -lsqlite3`. Output the violations in the order they appear in the JSON log. Ensure the CSV fields are comma-separated and do not contain extra spaces.