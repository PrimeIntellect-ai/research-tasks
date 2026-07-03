You are acting as a Database Administrator and Go developer. We have an SQLite database containing organizational hierarchy and sales data at `/home/user/company.db`. Due to a previous migration error, one of the indexes on the sales table is corrupted, making some direct recursive SQL queries unstable. 

Your task is to write a Go program that extracts the raw data, processes it in memory (or via safe queries), and generates a fully validated JSON report.

The database has two tables:
1. `employees` (id INTEGER PRIMARY KEY, name TEXT, manager_id INTEGER)
2. `sales` (id INTEGER PRIMARY KEY, emp_id INTEGER, amount REAL, sale_date TEXT)

You must write a Go program at `/home/user/generate_report.go` that accomplishes the following:
1. **Graph Materialization:** Calculate the `team_sales` for each employee. An employee's `team_sales` is the sum of their own personal sales plus the personal sales of *all* their direct and indirect reports (the entire subtree under them in the management graph).
2. **Window/Analytical Aggregation:** Calculate the `peer_rank` for each employee. The `peer_rank` is the rank of the employee's *personal total sales* compared to other employees who share the exact same `manager_id` (Rank 1 is the highest personal sales). In case of a tie in sales, the employee with the lower `emp_id` gets the better rank. Employees with no manager (NULL) are ranked among others with no manager.
3. **Output Schema Validation:** Your Go program must output a JSON array of objects to `/home/user/output.json`. The output must be sorted by `emp_id` ascending. It must strictly conform to the JSON schema provided at `/home/user/schema.json`.

The expected JSON objects should have the following keys:
- `emp_id` (integer)
- `name` (string)
- `team_sales` (number)
- `peer_rank` (integer)

You may use standard Go libraries and `github.com/mattn/go-sqlite3` for database access. Ensure your output exactly matches the schema and mathematical logic.