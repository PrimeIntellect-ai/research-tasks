You are an AI assistant helping a compliance officer audit an organization's internal network access patterns.

There is an SQLite database located at `/home/user/audit.db` containing two tables:
1. `employees` (`emp_id` INTEGER PRIMARY KEY, `name` TEXT, `manager_id` INTEGER)
2. `access_logs` (`log_id` INTEGER PRIMARY KEY, `emp_id` INTEGER, `resource_id` INTEGER, `bytes_transferred` INTEGER)

We suspect data exfiltration from a specific managerial branch. Your task is to write a C program (`/home/user/audit_processor.c`) that securely queries this database to identify anomalous access patterns.

The C program must:
1. Take exactly two command-line arguments (after the executable name): `<manager_id>` (integer) and `<bytes_threshold>` (integer).
2. Connect to `/home/user/audit.db` using the SQLite3 C API.
3. Use a safely **parameterized query** (`sqlite3_bind_int`) to prevent SQL injection.
4. Execute a single SQL query that:
   - Uses a **Recursive CTE** to find all subordinates (direct and indirect) of the given `<manager_id>`. (Include the manager themselves in the result).
   - Aggregates the total `bytes_transferred` per employee, per `resource_id`.
   - Uses a **Window Function** (`ROW_NUMBER()`) to rank these subordinates based on their total bytes transferred for each `resource_id`. The partition should be by `resource_id`, ordered by the total aggregated bytes in DESCENDING order, and then by `emp_id` in ASCENDING order to break ties.
   - Filters the aggregated results so that only records where the total `bytes_transferred` is strictly greater than `<bytes_threshold>` are kept.
   - Sorts the final result by `resource_id` ASC, and then by the calculated rank ASC.
5. Write the results to `/home/user/audit_results.csv` in the format: `emp_id,name,resource_id,total_bytes,rank` (include a header row).

Compile the program using:
`gcc -o /home/user/audit_processor /home/user/audit_processor.c -lsqlite3`

Once compiled, execute your program to audit manager `1` with a threshold of `500`:
`/home/user/audit_processor 1 500`

The automated test will verify the contents of `/home/user/audit_results.csv`.