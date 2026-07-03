You are acting as an assistant for a compliance officer who is auditing system access. 

We have a SQLite database at `/home/user/audit.db` containing three tables:
1. `departments`: `dept_id` (INTEGER), `name` (TEXT), `parent_dept_id` (INTEGER)
2. `employees`: `emp_id` (INTEGER), `name` (TEXT), `dept_id` (INTEGER)
3. `access_logs`: `log_id` (INTEGER), `emp_id` (INTEGER), `access_time` (TEXT), `resource` (TEXT)

There is a Python script at `/home/user/audit.py` that is supposed to fetch all access logs for employees in the "Finance" department AND all of its sub-departments (recursively, no matter how deep). 

However, the script has two major problems:
1. It is missing join conditions, resulting in an implicit cross join that returns incorrect, duplicated data.
2. It does not use a recursive query to find sub-departments, so it misses nested departments like "Payroll" or "Accounts Payable" which fall under "Finance".

Your task is to:
1. Fix the Python script `/home/user/audit.py` so that it uses a **Recursive CTE** to dynamically find the "Finance" department and all its hierarchical sub-departments.
2. Properly join the departments, employees, and access_logs tables to eliminate the cross join.
3. The Python script must execute the query and export the results to a CSV file at `/home/user/audit_results.csv`. The CSV must have exactly these headers: `EmployeeName,DepartmentName,AccessTime,Resource`. The results should be sorted by `AccessTime` in ascending order.
4. To optimize the audit process, write a SQL file at `/home/user/optimize.sql` containing a `CREATE INDEX` statement that optimizes the lookup of access logs by `emp_id` in the `access_logs` table. Name the index `idx_access_logs_emp_id`.

Ensure your corrected `audit.py` handles the data extraction and CSV formatting appropriately using Python's standard `sqlite3` and `csv` modules.