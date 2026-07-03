As a compliance officer, you are auditing the access control hierarchy of our corporate systems. You have been provided with an SQLite database at `/home/user/audit.db` containing two tables:
1. `employees` (`emp_id`, `name`, `manager_id`, `dept_id`) - Represents the management hierarchy. The CEO has `manager_id IS NULL`.
2. `permissions` (`dept_id`, `resource`) - Maps departments to their accessible system resources.

A previous engineer wrote a Python script at `/home/user/generate_report.py` to extract an audit report. However, the script is broken:
- It generates completely wrong results due to an implicit cross join between employees and permissions.
- It fails to compute the hierarchical management path for each employee.

Your task is to fix the Python script (or write a new one) to extract the correct compliance data and export it.

Requirements:
1. Use a Recursive CTE in your SQL query to traverse the management hierarchy starting from the CEO (`manager_id IS NULL`).
2. Calculate a `path` string for each employee representing their chain of command using `emp_id`s separated by `->` (e.g., the CEO's path is `"1"`, and a direct report's path might be `"1->2"`).
3. Correctly join the `permissions` table so that each employee is matched ONLY with the resource assigned to their specific `dept_id`.
4. The Python script must execute this query and export the results to a JSON file at `/home/user/compliance_graph.json`.
5. The JSON file must contain a list of dictionaries, sorted in ascending order by `emp_id`. 

The JSON array must have exactly this structure for each object:
```json
[
  {
    "emp_id": 1,
    "name": "Alice (CEO)",
    "resource": "All Systems",
    "path": "1"
  },
  ...
]
```

Run your script to produce the `/home/user/compliance_graph.json` file. Ensure the exported data is perfectly clean and the cross-join bug is eliminated.