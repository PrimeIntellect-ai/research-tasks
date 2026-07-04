You are acting as a compliance officer auditing an organization's resource access systems. 

A previous auditor left behind a broken Bash script that uses SQLite to analyze employee access to highly sensitive resources. Their query was supposed to identify potential insider threats by comparing an employee's access counts to their department's average, while also calculating a "co-access degree" (a basic graph centrality measure representing how many *other* employees accessed the exact same highly sensitive resources). 

However, their query contains an implicit cross join that causes a massive row explosion, returning wrong results. 

Your task is to create a fixed Bash script at `/home/user/run_audit.sh` that queries the SQLite database at `/home/user/audit.db`.

The script must execute a single SQLite query that outputs a CSV (with headers) containing the following columns, in order:
1. `emp_id`: The ID of the employee.
2. `name`: The name of the employee.
3. `department`: The employee's department.
4. `high_risk_accesses`: The total number of times the employee accessed resources with `sensitivity = 'HIGH'`.
5. `dept_avg_accesses`: The average number of HIGH sensitivity accesses among all employees in the *same department* who have at least one HIGH sensitivity access. (Use a window function. Round to 2 decimal places).
6. `co_access_degree`: The number of *distinct other employees* who accessed at least one of the exact same HIGH sensitivity resources as this employee.

Requirements for the query:
- Only include employees who have accessed at least one HIGH sensitivity resource.
- Fix the implicit cross-join logic.
- The output should be piped directly from `sqlite3` to a file at `/home/user/audit_report.csv`.
- Sort the final output by `co_access_degree` DESC, then `high_risk_accesses` DESC, then `emp_id` ASC.
- Ensure the bash script is executable.

You will need to explore `/home/user/audit.db` to understand the exact schema for the `employees`, `resources`, and `access_logs` tables. Write your bash script to automate the execution of the corrected query and export the results.