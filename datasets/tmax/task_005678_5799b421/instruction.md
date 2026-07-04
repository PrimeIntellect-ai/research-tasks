As a compliance officer, I need to audit our internal permissions structure. We have an SQLite database located at `/home/user/compliance.db` that contains our organizational hierarchy and system access logs. 

The database has two tables:
1. `employees`: `id` (INTEGER PRIMARY KEY), `name` (TEXT), `manager_id` (INTEGER)
2. `access_grants`: `employee_id` (INTEGER), `system_name` (TEXT)

An employee has "direct access" to a system if there is a record of them in the `access_grants` table for that system. 
An employee has "inherited access" if ANY of their managers, anywhere up the management chain (their manager, their manager's manager, etc.), has direct access to the system.

I need you to generate a report of all employees who have inherited access to the system named `'Project_Zeus'`, but who DO NOT have direct access themselves. 

Please perform the query and save the results to a CSV file at `/home/user/zeus_audit.csv`. 

Requirements for the CSV file:
- It must contain exactly two columns: `employee_id` and `employee_name`
- Include a header row: `employee_id,employee_name`
- Filter the results to only include employees with inherited access who lack direct access to 'Project_Zeus'.
- Sort the final results alphabetically by the employee's `name`.
- Paginate the results: I only want the first 5 records (offset 0, limit 5) matching this criteria.

You may use any programming language or tool (like a python script or direct sqlite3 shell commands) to chain this process together, as long as the final CSV file is perfectly formatted.