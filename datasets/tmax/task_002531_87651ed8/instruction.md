You are acting as a compliance officer auditing an organization's access logs to detect unauthorized system usage.

You have been provided with an SQLite database at `/home/user/audit_data.db` containing the access history and organizational graph. The database has the following tables (all currently without indexes):

- `employees`: `emp_id` (INT), `name` (TEXT), `department_id` (INT)
- `systems`: `sys_id` (INT), `sys_name` (TEXT), `owning_dept_id` (INT)
- `exceptions`: `emp_id` (INT), `sys_id` (INT) - Represents explicit cross-department access grants.
- `access_logs`: `log_id` (INT), `emp_id` (INT), `sys_id` (INT), `timestamp` (TEXT)

**Your Task:**
Write a Python script at `/home/user/audit.py` that performs the following:
1. **Index Strategy:** Connects to `/home/user/audit_data.db` and creates necessary indexes on the tables to optimize the queries (assume the real database could have millions of rows, so proper indexing on join/filter keys is required).
2. **Knowledge Graph Pattern Matching:** Identifies all "Compliance Violations". A violation occurs when an employee accesses a system owned by a department *other* than their own, AND there is NO matching record in the `exceptions` table for that `(emp_id, sys_id)` pair.
3. **Cross-Query Aggregation:** Aggregates the total number of violations per employee.
4. **Output:** Writes the summarized results to `/home/user/compliance_report.json`.

The output file `/home/user/compliance_report.json` must be a JSON array of objects, containing ONLY the employees who have at least 1 violation. The objects must have the following keys:
- `emp_id` (integer)
- `name` (string)
- `violation_count` (integer)

Sort the JSON array by `violation_count` descending. If there is a tie, sort by `emp_id` ascending.

Execute your script to produce the final JSON file.