You are a data engineer debugging an ETL pipeline. We extract organizational hierarchy data from a local SQLite database (`/home/user/data.db`). 

Recently, the database suffered a partial disk fault, and while the table data is intact, the index `idx_manager` on the `employees` table is known to occasionally return stale or ghost rows when traversed. 

Your task is to write a Python script (`/home/user/etl_extract.py`) that performs the following steps:
1. Connects to the SQLite database at `/home/user/data.db`.
2. Repairs the index by running the SQLite `REINDEX;` command (or specifically `REINDEX idx_manager;`) before running any `SELECT` queries.
3. Uses a **Recursive CTE** (Common Table Expression) to extract the complete management chain for the employee with `id = 845`, moving *bottom-up* from employee 845 up to the CEO (who has no manager).
4. The query must join the `departments` table to include the department name for each person in the chain.
5. Exports the results to `/home/user/audit_chain.json`.

The output JSON file must be a JSON array of objects, ordered from the target employee (level 0) up to the CEO (level N). Each object must exactly match this structure:
```json
[
  {
    "level": 0,
    "employee_id": 845,
    "employee_name": "Target Employee",
    "department_name": "Engineering",
    "manager_id": 404
  },
  ...
]
```
*(Note: `manager_id` should be `null` for the CEO).*

Database Schema:
- `departments` (id INTEGER PRIMARY KEY, name TEXT)
- `employees` (id INTEGER PRIMARY KEY, name TEXT, manager_id INTEGER, dept_id INTEGER, salary INTEGER)

You are free to use standard Python libraries (`sqlite3`, `json`). Execute your script to ensure `/home/user/audit_chain.json` is successfully created and correctly formatted.