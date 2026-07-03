You are assisting a compliance officer who is auditing system access logs across a company's organizational hierarchy. 

There is an SQLite database located at `/home/user/audit.db` containing two tables:
1. `employees`:
   - `emp_id` (INTEGER PRIMARY KEY)
   - `name` (TEXT)
   - `manager_id` (INTEGER) - refers to `emp_id` of the manager. The CEO has `manager_id = NULL`.
2. `access_logs`:
   - `log_id` (INTEGER PRIMARY KEY)
   - `emp_id` (INTEGER)
   - `system_name` (TEXT)
   - `access_date` (DATE)

The compliance officer needs a Python script located at `/home/user/generate_report.py` that queries this database and outputs a strict JSON report to `/home/user/compliance_report.json`.

Your Python script must execute a SQL query (or queries) that performs the following:
1. Uses a **Recursive CTE** to determine each employee's `hierarchy_level` (The CEO with `manager_id IS NULL` is level 0, their direct reports are level 1, and so on).
2. Uses **Window Functions** to determine the most frequently accessed system (`top_system`) for each employee, along with the number of times they accessed it (`top_system_access_count`). If there is a tie in access counts, pick the system that comes first alphabetically. Employees with no access logs should not be included in the final report.
3. Joins these insights together.

The output at `/home/user/compliance_report.json` must be a JSON array of objects, strictly adhering to this schema and ordered by `employee_id` ascending:
```json
[
  {
    "employee_id": 2,
    "hierarchy_level": 1,
    "top_system": "Vault",
    "top_system_access_count": 5
  },
  ...
]
```

Write the Python script, execute it, and ensure the resulting JSON file is perfectly formatted.