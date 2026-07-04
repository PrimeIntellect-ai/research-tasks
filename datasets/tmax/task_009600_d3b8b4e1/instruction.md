You are assisting a compliance officer in auditing system access records. An SQLite database containing company records and system access logs has been provided at `/home/user/audit.db`.

Your task is to analyze the schema of this database, map the relationships between the tables, and construct a Bash script that extracts a specific set of security violations. 

A "security violation" occurs when an employee accesses a system for which they do not possess the required clearance level (i.e., the employee's `clearance_level` is strictly less than the system's `required_clearance`).

Perform the following steps:
1. Explore the schema of `/home/user/audit.db` to understand the tables representing employees, departments, system clearances, and access logs.
2. Create a Bash script at `/home/user/generate_audit_report.sh`.
3. The script must execute an SQL query against `/home/user/audit.db` to find all security violations.
4. The script must output the findings to `/home/user/violations.csv` in exactly this CSV format (without headers):
   `employee_name,department_name,system_name,access_time`
5. The output must be sorted chronologically by `access_time` in ascending order.
6. Make sure your script is executable.

Ensure your query effectively joins the necessary tables to resolve employee names, department names, and system requirements.