You are assisting a compliance officer in auditing system access records. 

An SQLite database is located at `/home/user/audit.db`. We suspect there are compliance violations where employees were granted access to systems for which they lacked valid certifications, or their certifications had expired at the time of access. We do not have the exact database schema documentation, so you will need to inspect the database to understand the tables and their relationships.

Your task is to:
1. Analyze the schema of `/home/user/audit.db` to identify how employees, access logs, and certifications are linked.
2. Write and execute a Python script at `/home/user/audit_check.py` that queries the database to identify all compliance violations. 
3. A compliance violation occurs when:
   - An access attempt has a status of 'GRANTED'
   - AND the employee either has NO certification for that specific system, OR the `access_time` of the log entry is strictly greater than the `expiration_date` of their certification for that system.
4. Your Python script must export the resulting violations to `/home/user/violations.json`.

The output `/home/user/violations.json` must be a JSON array of objects, with each object containing exactly the following keys:
- `log_id` (integer)
- `emp_id` (integer)
- `name` (string, the employee's name)
- `system_name` (string)
- `access_time` (string)

The JSON array must be sorted in ascending order by `log_id`. Ensure your Python script properly formats and outputs this file.