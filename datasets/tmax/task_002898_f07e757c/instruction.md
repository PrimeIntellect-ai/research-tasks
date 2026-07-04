You are acting as a compliance officer auditing an organization's access controls and permissions. You have been provided with an SQLite database containing organizational hierarchy, employee permissions, and access logs. 

Your objective is to write a Python script `/home/user/audit_report.py` that queries this database to identify compliance violations and outputs a report to `/home/user/compliance_report.json`. You must also optimize the database so the queries run efficiently.

**Database Schema (`/home/user/audit.db`):**
1. `employees` table:
   - `id` (INTEGER PRIMARY KEY)
   - `name` (TEXT)
   - `manager_id` (INTEGER, foreign key referencing `employees.id`)
   - `permissions` (TEXT, a JSON array of permission strings)

2. `access_logs` table:
   - `id` (INTEGER PRIMARY KEY)
   - `employee_id` (INTEGER, foreign key referencing `employees.id`)
   - `resource_owner_id` (INTEGER, foreign key referencing `employees.id`)
   - `timestamp` (DATETIME, format 'YYYY-MM-DD HH:MM:SS')
   - `action` (TEXT)

**Compliance Violations to Identify:**
1. **Unauthorized Access (Hierarchy Bypass):** An employee accessed a resource owned by another employee, but the accessor is NOT in the direct management chain above the resource owner, AND the accessor is not the resource owner themselves. (e.g., if A manages B, and B manages C, A can access C's resources, but C cannot access A's, and B cannot access a peer's). 
2. **Anomalous Volume:** An employee who has made more than 5 accesses within *any* rolling 3-day window (i.e., looking at the preceding 3 days for each access log entry). 
3. **Toxic Permissions:** An employee whose `permissions` JSON array contains both `"APPROVE_FUNDS"` and `"REQUEST_FUNDS"`.

**Requirements:**
1. Your Python script `/home/user/audit_report.py` must execute the necessary SQL queries to find these violations.
2. The script must save the results to `/home/user/compliance_report.json` with the following exact structure (all lists must contain integers sorted in ascending order):
```json
{
  "unauthorized_access_log_ids": [1, 5, 12, ...],
  "anomalous_employee_ids": [3, 9, ...],
  "toxic_employee_ids": [2, 15, ...]
}
```
3. **Optimization:** The database is reasonably large, and your queries might be slow. Your Python script should include SQL statements to create appropriate indexes on the tables to optimize these specific queries before executing them.
4. Save the `EXPLAIN QUERY PLAN` output for your "Unauthorized Access" query to `/home/user/query_plan.txt`.