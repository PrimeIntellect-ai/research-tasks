You are assisting a compliance officer auditing an organization's access control systems. The organization determines system access based on an employee's assigned roles, but with a hierarchical twist: **managers automatically inherit all access rights possessed by any of their direct or indirect subordinates**.

The compliance officer has provided an SQLite database at `/home/user/compliance.db` containing the organization's structure and access policies. They have also written a Python script at `/home/user/audit_access.py` to identify every employee who has access to the highly sensitive system named `Project_Zeus`.

However, the Python script is currently returning incorrect results. The script uses a recursive Common Table Expression (CTE) to traverse the employee hierarchy, but the query contains a logical flaw (an implicit cross join due to a missing join condition in the recursive step). This causes the query plan to explode and incorrectly report that almost everyone has access to `Project_Zeus`.

Your task:
1. Analyze the SQLite database schema and the query execution plan in `/home/user/audit_access.py`.
2. Fix the SQL query inside `/home/user/audit_access.py` so that it correctly computes the hierarchical access graph. It must only traverse true manager-to-subordinate relationships.
3. Run the fixed script. It should write its results to `/home/user/zeus_audit.csv`.

The output file `/home/user/zeus_audit.csv` must contain a header `employee_name,system_name` followed by the alphabetically sorted names of only the employees who actually have access (directly or inherited) to `Project_Zeus`.