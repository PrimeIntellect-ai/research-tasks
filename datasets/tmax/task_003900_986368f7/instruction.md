You are assisting a compliance officer in auditing system access logs. We need a reusable tool to query our internal SQLite audit database to find specific suspicious access patterns.

The database is located at `/home/user/audit.db` and contains three tables:
1. `employees` (id INTEGER PRIMARY KEY, name TEXT, department TEXT)
2. `access_logs` (id INTEGER PRIMARY KEY, emp_id INTEGER, resource TEXT, access_timestamp DATETIME)
3. `auth_logs` (id INTEGER PRIMARY KEY, emp_id INTEGER, ip_address TEXT, auth_timestamp DATETIME)

Your task is to write a Python script at `/home/user/audit_query.py` that queries this database and outputs the results to a JSON file.

Requirements for `/home/user/audit_query.py`:
1. Use the standard `sqlite3` and `argparse` modules.
2. Accept the following command-line arguments:
   * `--resource`: The exact resource path accessed.
   * `--ip-prefix`: The starting characters of the IP address to filter by.
   * `--limit`: The maximum number of records to return (integer).
   * `--offset`: The number of records to skip (integer).
3. The script must execute a single query (using proper parameterization to prevent SQL injection) that:
   * Joins the three tables on the employee ID.
   * Filters for employees strictly in the 'Engineering' department.
   * Filters for `access_logs.resource` exactly matching the `--resource` argument.
   * Filters for `auth_logs.ip_address` starting with the `--ip-prefix` argument.
   * Sorts the results first by `access_timestamp` DESCENDING, then by `auth_timestamp` DESCENDING, and finally by `name` ASCENDING.
   * Applies the `--limit` and `--offset` for pagination.
4. The script must write the final result to `/home/user/report.json` as a JSON array of objects. Each object must have exactly these keys:
   `"name"`, `"resource"`, `"access_timestamp"`, `"ip_address"`, `"auth_timestamp"`.

Ensure your script handles the arguments correctly and executes without error when invoked. Do not create the database yourself; assume it already exists.