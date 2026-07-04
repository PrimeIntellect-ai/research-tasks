You are a database administrator tasked with fixing a reporting pipeline. 

The company's HR application reads employee hierarchy and salary data from an SQLite database located at `/home/user/company_data.db`. Recently, the system has been generating incorrect organizational charts and budget reports because the `current_employees` materialized table has corrupted indexes and contains stale data. 

Instead of relying on the broken materialized table, you need to build a robust data pipeline in Python that derives the correct state directly from the immutable `employee_events` append-only log table.

The `employee_events` table tracks all changes to employee records over time. Its schema is:
- `event_id` (INTEGER PRIMARY KEY)
- `emp_id` (INTEGER)
- `manager_id` (INTEGER, nullable)
- `salary` (INTEGER)
- `status` (VARCHAR) - either 'active' or 'terminated'
- `event_timestamp` (DATETIME)

Your task is to write a Python script at `/home/user/process_org.py` that does the following:
1. Connects to `/home/user/company_data.db`.
2. Bypasses the stale tables and reads only from `employee_events`.
3. Uses a query with window functions to resolve the *latest* event for each `emp_id` (based on `event_timestamp`). Filter the results to only include employees whose latest status is 'active'.
4. Uses a recursive CTE (or equivalent hierarchical processing) to calculate the `total_org_salary` for each active employee. An employee's `total_org_salary` is defined as their own salary plus the salaries of all their direct and indirect active reports (i.e., the entire subtree of active employees reporting up to them).
5. Maps this relational data into a JSON document. The script should export a list of dictionaries to `/home/user/org_metrics.json`. 

The output JSON file must strictly be a JSON array of objects, sorted in ascending order by `emp_id`. Each object must have the following format:
```json
[
  {
    "emp_id": 1,
    "salary": 150000,
    "total_org_salary": 450000
  },
  ...
]
```

Requirements:
- Ensure your Python script executes successfully and generates the exact JSON structure requested.
- You must rely on the SQLite database engine to do the heavy lifting for the latest-state resolution and hierarchical queries where possible, but you may use Python for pipeline chaining and final JSON formatting.
- Do not modify the original database file.