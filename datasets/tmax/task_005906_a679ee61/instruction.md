You are acting as a Database Administrator optimizing a data extraction pipeline. 

We have data split across two formats:
1. An SQLite database at `/home/user/company.db` containing an `employees` table (columns: `id` INTEGER, `name` TEXT, `manager_id` INTEGER, `dept_id` INTEGER). The `manager_id` references the `id` of the employee's direct manager.
2. A JSON Lines file at `/home/user/departments.jsonl` containing department details (keys: `dept_id` (int), `dept_name` (string), `budget` (int)).

Your task is to write a Python script at `/home/user/query_pipeline.py` that reads from both sources, performs an in-memory join, and extracts a specific graph pattern: managers who have direct reports, but ONLY if the manager's department has a budget strictly greater than `500000`.

The script must output the results to a JSON file at `/home/user/optimized_reports.json`.

The output MUST be a JSON array of objects, strictly adhering to this schema:
```json
[
  {
    "manager": "String (Name of the manager)",
    "department": "String (Name of the department)",
    "reports": ["String (Name of report 1)", "String (Name of report 2)", "..."]
  }
]
```
The array should be sorted alphabetically by the `manager`'s name. The `reports` array inside each object must also be sorted alphabetically.

Write the Python script, execute it, and ensure `/home/user/optimized_reports.json` is created with the exact correct structure and data.