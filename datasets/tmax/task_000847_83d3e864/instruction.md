You are a data engineer building a lightweight, dependency-free ETL pipeline using only Bash and standard POSIX utilities (like `awk`, `sed`, `join`, `sort`, etc.). 

You have been provided with two CSV files representing an organization's employee hierarchy and payroll:

1. `/home/user/employees.csv` - Contains employee details.
Format: `id,name,department,salary`

2. `/home/user/reporting.csv` - Contains the management hierarchy (directed edges from employee to manager).
Format: `emp_id,manager_id`

Your task is to write a bash script at `/home/user/etl.sh` that processes these files and calculates organizational metrics. The script must execute without any arguments and produce a final report at `/home/user/manager_summary.csv`.

The final report must contain a row for every employee who manages at least one person, with the following columns:
`manager_id,manager_name,department,direct_reports_count,total_descendant_salary`

Where:
- `direct_reports_count`: The number of employees who directly report to this manager.
- `total_descendant_salary`: The sum of the salaries of ALL employees in this manager's entire downstream hierarchy (both direct reports and indirect reports/descendants).

Requirements for `/home/user/manager_summary.csv`:
1. It must include a header row exactly as specified above.
2. It must be sorted numerically by `manager_id`.
3. It must be a valid comma-separated values file.
4. You must implement the graph traversal and aggregations using only standard Unix tools (e.g., `awk`, `bash`, `join`, etc.). No external databases or high-level languages like Python are allowed.

Ensure `/home/user/etl.sh` is executable and creates the required output file when run.