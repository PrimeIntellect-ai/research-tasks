You are acting as a compliance officer auditing an internal data access system.

You have been provided with an SQLite database file at `/home/user/audit.db` containing three tables, but the exact schema documentation has been lost. You will need to reverse-engineer the schema by inspecting the database directly. We know it contains information about employees, system resources, and access logs.

There is a strict compliance rule in place regarding highly sensitive resources:
**Rule:** A resource with a `sensitivity_level` of 3 can ONLY be accessed by an employee if that employee is in the 'Compliance' department, OR if any manager in their direct upward reporting chain (their manager, their manager's manager, etc.) is in the 'Compliance' department.

Your task is to:
1. Analyze the schema of `/home/user/audit.db` and understand how employees relate to managers (hierarchical graph), resources, and access logs.
2. Write a Python script at `/home/user/find_violations.py` that connects to this database.
3. The script must execute a single, efficient SQL query (using a recursive CTE to traverse the management hierarchy, along with complex joins) to identify all access log entries that violate the compliance rule mentioned above.
4. The Python script must output these violations to a JSON file at `/home/user/violations.json`.

The output file `/home/user/violations.json` must contain a JSON array of objects, sorted by the access log ID in ascending order. Each object must have exactly these keys:
- `log_id` (integer): The ID of the access log entry.
- `employee_name` (string): The name of the employee who made the unauthorized access.
- `resource_name` (string): The name of the resource they accessed.

Example of expected JSON format:
```json
[
  {
    "log_id": 12,
    "employee_name": "Jane Smith",
    "resource_name": "Q4_Financial_Projections"
  }
]
```

Do not modify the database. Write the script, run it, and ensure the resulting JSON file is perfectly formatted.