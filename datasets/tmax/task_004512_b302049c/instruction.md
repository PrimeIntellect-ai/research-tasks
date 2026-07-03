You are assisting a compliance officer who is auditing internal system accesses. We need to identify potential security anomalies where employees access restricted assets belonging to departments other than their own. 

An SQLite database is located at `/home/user/compliance.db`. It contains the following tables:
- `departments` (`dept_id` INTEGER PRIMARY KEY, `dept_name` TEXT)
- `employees` (`emp_id` INTEGER PRIMARY KEY, `name` TEXT, `dept_id` INTEGER)
- `restricted_assets` (`asset_id` INTEGER PRIMARY KEY, `asset_name` TEXT, `owning_dept_id` INTEGER)
- `access_logs` (`log_id` INTEGER PRIMARY KEY, `emp_id` INTEGER, `asset_id` INTEGER, `access_time` DATETIME)

Your task is to write a Python script `/home/user/audit.py` that fulfills these requirements:
1. Uses the `argparse` module to accept three arguments: `--start` (YYYY-MM-DD), `--end` (YYYY-MM-DD), and `--dept` (String, name of the department).
2. Connects to `/home/user/compliance.db`.
3. Creates necessary database indexes to optimize the audit query (ensure you use `IF NOT EXISTS`).
4. Constructs a **parameterized query** to find all access logs where:
   - The access occurred strictly between the `--start` and `--end` dates (inclusive of the start and end dates, assuming times fall on those days).
   - The employee belongs to the department specified by `--dept`.
   - The asset accessed is owned by a department *other* than the employee's department.
5. Writes the SQLite `EXPLAIN QUERY PLAN` output for this exact parameterized `SELECT` query into `/home/user/plan.txt`.
6. Executes the query and writes the results to `/home/user/results.csv` in standard CSV format, including a header row. The columns must be exactly: `log_id,emp_name,asset_name,access_time`.

Order the results in the CSV by `access_time` in ascending order. If two records have the same time, order by `log_id` ascending.

Make sure your script correctly runs with standard Python 3 and the built-in `sqlite3` and `csv` modules. The automated test will invoke your script with specific parameters to verify the outputs.