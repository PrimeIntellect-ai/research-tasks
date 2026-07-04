You are a database administrator tasked with analyzing an organizational hierarchy. The company data is stored in an SQLite database located at `/home/user/company.db`.

You need to write a Bash script at `/home/user/analyze_org.sh` that uses the `sqlite3` CLI tool to execute an advanced query combining recursive hierarchies and analytical window functions, and then exports the result to a CSV file.

The `company.db` database contains a single table:
`employees (id INTEGER PRIMARY KEY, name TEXT, department TEXT, salary INTEGER, manager_id INTEGER)`

Your script must execute a query that does the following:
1. Calculates the "management depth" of each employee using a Recursive CTE. The CEO (who has a `manager_id` of NULL) is at depth 0. Direct reports to the CEO are at depth 1, their direct reports are at depth 2, and so on.
2. Calculates the average salary of each employee's department using a Window Function.
3. Filters the results to only include employees who meet BOTH of the following conditions:
   - Their management depth is 2 or greater.
   - Their salary is strictly greater than the average salary of their department.
4. Sorts the final results first by `depth` descending, and then by `salary` descending.

Your script must export the final output to `/home/user/high_earners.csv` as a comma-separated values (CSV) file WITH headers. 
The CSV must have the following exact columns in this order:
`name,department,salary,depth,dept_avg_salary`

Ensure your script is executable (`chmod +x /home/user/analyze_org.sh`) and completely self-contained. When run, it should cleanly generate the `/home/user/high_earners.csv` file without any manual user input.