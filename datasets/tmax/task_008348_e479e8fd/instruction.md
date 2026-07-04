You are acting as a compliance officer auditing a company's internal system accesses. You have two disparate data sources that need to be cross-referenced to identify security violations. 

You are provided with:
1. An SQLite database at `/home/user/access_logs.db` containing two tables:
   - `employees` (`emp_id` INTEGER, `name` TEXT, `dept_id` TEXT)
   - `logs` (`log_id` INTEGER, `emp_id` INTEGER, `resource_id` TEXT, `access_time` TEXT, `status` TEXT)
2. A JSON document at `/home/user/resources.json` representing a NoSQL-style collection of resource access rules. It contains an array of objects, each with a `"resource_id"` and an `"allowed_depts"` array (listing department IDs authorized to access the resource).

Your task is to:
1. Write and execute a Python script `/home/user/audit.py` that cross-references the SQL database and the JSON document to find all compliance violations. A violation occurs when a log entry has a `status` of `'SUCCESS'` but the employee's `dept_id` is NOT in the `allowed_depts` for that `resource_id` in the JSON document.
2. The script must aggregate the violations and output a CSV file at `/home/user/violations.csv`. The CSV must have exactly this header: `emp_id,resource_id,violation_count`. Sort the rows by `emp_id` ascending, then by `resource_id` ascending.
3. The query performance on the `logs` table is currently slow when filtering by `status` and joining with `employees`. Create a file at `/home/user/index.sql` containing exactly one `CREATE INDEX` statement that creates a composite index to optimize the lookup of successful logs by `emp_id`. The index should be named `idx_logs_emp_status`.

Ensure all requested files are created at their exact paths.