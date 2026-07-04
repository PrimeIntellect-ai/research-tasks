You are acting as a compliance officer auditing system access logs. We have data scattered across multiple formats that needs to be unified and analyzed to find access violations.

The data consists of:
1. A relational SQLite database at `/home/user/data/hr.db` containing two tables:
   - `employees` (id INTEGER, name TEXT, department TEXT)
   - `resources` (id INTEGER, name TEXT, department_owner TEXT)
2. A JSON document store of access logs at `/home/user/data/access_logs.json`. This is a list of objects like `{"user_id": 1, "resource_id": 101, "timestamp": "2023-10-01T10:00:00Z"}`.
3. A JSON document of explicit cross-department authorizations at `/home/user/data/authorizations.json`. This is a list of objects like `{"user_id": 1, "resource_id": 102}`.

Your task is to:
1. Write a Python script `/home/user/audit.py` that ingests these three data sources.
2. Materialize a graph/mapping of which users accessed which resources.
3. Identify access violations. An access event is a violation if the resource's `department_owner` is different from the user's `department`, AND there is no corresponding explicit authorization in `authorizations.json` for that specific `user_id` and `resource_id`.
4. Aggregate and summarize the total number of violations grouped by the **user's department**.
5. The script must output this summary to `/home/user/violations_summary.json` as a simple JSON object mapping the department name (string) to the total count of violations (integer). For example: `{"Sales": 2, "Engineering": 1}`. Do not include departments with 0 violations.

Run your script to generate `/home/user/violations_summary.json`.