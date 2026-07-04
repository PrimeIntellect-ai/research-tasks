You are a data engineer tasked with building a bash-based ETL extraction pipeline and schema validator.

You have been given an SQLite database at `/home/user/company.db` containing two tables:
1. `employees` (id INTEGER PRIMARY KEY, name TEXT)
2. `reporting` (assignment_id INTEGER PRIMARY KEY, emp_id INTEGER, manager_id INTEGER, assigned_date TEXT)

Due to a past buggy migration, the `reporting` table has a "stale row" issue. Some employees have multiple reporting records. The true, active manager for an employee is the one in the `reporting` row with the most recent (maximum) `assigned_date`. The CEO has no reporting record (or manager_id is NULL).

Your task is to:
1. Write a bash script `/home/user/extract.sh` that queries `/home/user/company.db` using `sqlite3`. 
   - The query must use a recursive CTE to build an organizational hierarchy.
   - It must filter out the stale rows, only using the most recent `reporting` record for each employee.
   - The hierarchy should compute a `depth` (CEO is 0, direct reports to CEO are 1, etc.) and a `path` (a string of names joined by ` -> `, e.g., `Alice -> Bob -> Charlie`).
   - The output must be written to `/home/user/org_chart.json` as a JSON array of objects with the keys: `emp_id` (integer), `name` (string), `manager_id` (integer or null for CEO), `depth` (integer), and `path` (string). 
   - You can use SQLite's native JSON output options (`-json`).

2. Write a bash script `/home/user/validate.sh` that reads an arbitrary JSON file path provided as its first argument (e.g., `./validate.sh /home/user/org_chart.json`) and validates the schema using `jq`.
   - It must ensure the root is a JSON array.
   - It must ensure every object in the array contains exactly the keys `emp_id`, `name`, `manager_id`, `depth`, and `path`.
   - It must ensure `depth` is a number and `path` is a string.
   - The script should exit with status `0` if the schema is valid, and exit `1` and print an error message to stdout if it is invalid.

Both scripts must be executable. Do not install any external tools; use standard bash, coreutils, `sqlite3`, and `jq`.