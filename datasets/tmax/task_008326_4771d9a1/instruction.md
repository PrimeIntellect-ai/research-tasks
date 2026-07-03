You are an AI assistant helping a compliance officer perform a system audit. 

We have an SQLite database at `/home/user/compliance.db` that tracks corporate asset ownership. We suspect the database has an inefficient or corrupted index (`idx_employee_assets`) that has been causing queries to stall or return incorrect historical data during full table scans. 

Your task is to write a Rust application that cleans up the database indexes, executes a recursive hierarchical query, and outputs a consolidated compliance report in JSON format.

Here is the schema of the database:
`employees` (id INTEGER PRIMARY KEY, name TEXT, manager_id INTEGER)
`assets` (id INTEGER PRIMARY KEY, employee_id INTEGER, asset_tag TEXT, value INTEGER)

Please perform the following steps:
1. Initialize a new Rust project in `/home/user/audit_tool`.
2. Write a Rust program that connects to `/home/user/compliance.db`.
3. In your Rust code, first execute a SQL command to `DROP INDEX IF EXISTS idx_employee_assets;`.
4. Create a new, optimized index named `idx_assets_emp_val` on the `assets` table covering `(employee_id, value DESC)`.
5. Write and execute a single query (using a Recursive CTE) that:
   - Starts with the root employee (employee ID 1).
   - Recursively finds all employees under this root (the entire company hierarchy).
   - Joins with the `assets` table.
   - Aggregates the data to calculate the `total_asset_value` and `asset_count` for *each* employee in the hierarchy. (If an employee has no assets, they should still appear with 0 value and 0 count).
6. Map this relational result into a structured format and serialize it to a JSON file at `/home/user/audit_report.json`.

The output JSON must be a JSON array of objects, sorted by `total_asset_value` DESCENDING. If there is a tie, sort by `employee_id` ASCENDING.

Required JSON structure for `/home/user/audit_report.json`:
```json
[
  {
    "employee_id": 2,
    "name": "Bob",
    "total_asset_value": 4500,
    "asset_count": 2
  },
  {
    "employee_id": 1,
    "name": "Alice",
    "total_asset_value": 1200,
    "asset_count": 1
  }
]
```

Build and run your Rust program so that the final `audit_report.json` is generated successfully.