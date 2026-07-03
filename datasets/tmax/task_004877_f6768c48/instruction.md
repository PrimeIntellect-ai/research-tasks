As a compliance officer auditing our internal systems, I need to generate an access risk report based on our corporate directory and access logs. 

We have an SQLite database located at `/home/user/corporate.db`. It contains two tables:
1. `employees(id INTEGER PRIMARY KEY, name TEXT, manager_id INTEGER, department TEXT)`
2. `access_logs(log_id INTEGER PRIMARY KEY, emp_id INTEGER, resource TEXT, status TEXT, timestamp DATETIME)`

The database is currently unoptimized and queries against the logs are slow. 

Please write a C++ program at `/home/user/process_audit.cpp` that does the following:
1. Connects to `/home/user/corporate.db` using the SQLite C/C++ API.
2. Creates an index named `idx_emp_status` on the `access_logs` table covering `emp_id` and `status` to optimize the query plan.
3. Executes a single complex SQL query that:
   - Uses a **Recursive CTE** to find all employees in the hierarchy starting from the CEO (`id = 1`) and calculates their `depth` in the organizational chart (CEO is depth 0, direct reports are depth 1, etc.).
   - Joins these employees with `access_logs` to calculate the total number of `status = 'DENIED'` events for each employee (let's call this `denied_count`). Employees with no denied logs should have a count of 0.
   - Uses a **Window Function** to calculate the `dept_rank` of each employee within their `department` based on their `denied_count` (highest count gets rank 1). If there is a tie in counts, order by the employee's `id` ascending.
4. Writes the results of this query to a CSV file at `/home/user/audit_report.csv`.

The CSV must have a header row and follow this exact format and column order:
`emp_id,name,department,depth,denied_count,dept_rank`

You will need to install any necessary development packages to compile your C++ code with SQLite3. Compile your program to `/home/user/process_audit` and execute it so the CSV file is generated. Ensure your C++ program gracefully handles database connection and query execution errors.