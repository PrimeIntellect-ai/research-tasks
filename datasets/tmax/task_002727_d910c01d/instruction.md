You are helping a data analyst who is struggling with a buggy bash script. 

The analyst wrote a script located at `/home/user/generate_report.sh`. This script imports two CSV files (`/home/user/employees.csv` and `/home/user/departments.csv`) into an SQLite database and attempts to query them to create an organizational chart. However, the current SQL query inside the bash script is missing a join condition, resulting in an implicit cross join (Cartesian product), and it completely fails to resolve the management hierarchy.

Your task is to fix the bash script `/home/user/generate_report.sh` so that it correctly joins the data and uses a recursive query (CTE) to build the organizational hierarchy. 

The modified script must export the final query results to `/home/user/org_chart.csv` with the following columns (with a header row):
`emp_id,name,dept_name,manager_name,management_chain`

Requirements for the data:
1. `emp_id`: The employee's ID.
2. `name`: The employee's name.
3. `dept_name`: The correct department name for the employee (fixing the cross join).
4. `manager_name`: The name of the employee's direct manager (leave empty if they have no manager).
5. `management_chain`: A string showing the hierarchy path from the top-level manager down to the employee, separated by `->` (e.g., `Alice->Bob->Dave`. If the employee is at the top, it should just be their name, e.g., `Alice`).

Run the fixed script so that `/home/user/org_chart.csv` is generated successfully. Ensure the CSV output strictly uses commas as delimiters and includes the header.