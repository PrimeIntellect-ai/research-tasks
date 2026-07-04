As a compliance officer, I need your help auditing our corporate expense system. We suspect that certain employees are abusing their expense accounts, and I need a reliable, repeatable tool to identify them. 

You have been provided with an SQLite database at `/home/user/audit.db`. It contains two tables:
1. `employees`
   - `id` (INTEGER PRIMARY KEY)
   - `name` (TEXT)
   - `manager_id` (INTEGER, references `id`, NULL for the CEO)

2. `expenses`
   - `id` (INTEGER PRIMARY KEY)
   - `emp_id` (INTEGER, references `employees.id`)
   - `amount` (REAL)
   - `timestamp` (TEXT)

Please write a Rust program that queries this database to identify the top spenders within each direct manager's team.

Your Rust application must:
1. Be created as a Cargo project in `/home/user/audit_tool`.
2. Use a single, optimized SQL query (utilizing Common Table Expressions for graph/hierarchy traversal if necessary, and Window Functions for analytical aggregation) to calculate the total expenses for each employee and rank them within their manager's group (partitioned by `manager_id`, ordered by total expenses descending).
3. Filter the results to include ONLY employees who rank in the top 2 for their manager's team AND whose total expenses strictly exceed $10,000.
4. Output the results to a precisely formatted JSON file at `/home/user/suspicious_report.json`. 

The output JSON must be an array of objects, sorted ascending by `manager_id`, and then descending by `total_spent`. The JSON schema for each object must be exactly:
```json
{
  "employee_name": "String",
  "manager_id": "Integer",
  "total_spent": "Float",
  "team_rank": "Integer"
}
```

Ensure your Rust code handles the database connection safely and formats the JSON properly. Do not hardcode the employee names or amounts in your Rust code; it must dynamically query the database. Run your compiled Rust program to generate the report file.