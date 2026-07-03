You are assisting a compliance officer auditing an internal corporate network. We have an SQLite database located at `/home/user/audit.db` containing employee records, system classifications, and access logs. 

Your task is to create a Python script at `/home/user/extract_violations.py` that queries this database to identify all **unauthorized access events**, exports them to a specifically formatted JSON file, and then validates the output schema.

Here is the database schema:
1. `employees` table:
   - `emp_id` (INTEGER PRIMARY KEY)
   - `name` (TEXT)
   - `clearance_level` (INTEGER)
   - `termination_date` (TEXT, 'YYYY-MM-DD' format, NULL if still employed)

2. `systems` table:
   - `sys_id` (INTEGER PRIMARY KEY)
   - `sys_name` (TEXT)
   - `required_clearance` (INTEGER)

3. `access_logs` table:
   - `log_id` (INTEGER PRIMARY KEY)
   - `emp_id` (INTEGER)
   - `sys_id` (INTEGER)
   - `access_timestamp` (TEXT, 'YYYY-MM-DD HH:MM:SS' format)

An access event is considered **unauthorized** if EITHER of the following conditions is met:
1. **TERMINATED**: The `access_timestamp` occurs strictly after the employee's `termination_date` (compare the date portion of `access_timestamp` to `termination_date`).
2. **CLEARANCE**: The employee's `clearance_level` is strictly less than the system's `required_clearance`.
*Note: If an event violates both conditions, classify the violation type as "TERMINATED".*

Your Python script must execute a single SQLite query (using complex joins/subqueries) to find these records, and export the results to `/home/user/violations.json`. 

The output JSON must be a list of objects, each containing exactly these keys:
- `log_id` (integer)
- `employee_name` (string)
- `system_name` (string)
- `violation_type` (string, either "TERMINATED" or "CLEARANCE")

Sort the JSON array in ascending order by `log_id`.

Additionally, create a shell script at `/home/user/run_pipeline.sh` that:
1. Runs your Python script (`python3 extract_violations.py`).
2. Validates the resulting `violations.json` structure using a small inline Python snippet (ensure it parses as valid JSON and is a list). It should print "Pipeline successful" and exit with 0 if valid.

Ensure the bash script is executable. Run `/home/user/run_pipeline.sh` to produce the final `violations.json`.