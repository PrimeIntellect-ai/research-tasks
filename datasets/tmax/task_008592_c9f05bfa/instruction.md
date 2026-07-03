As a compliance officer, I am auditing our internal systems following a potential insider threat incident involving a senior manager. I need you to correlate our organizational hierarchy with system access logs to determine the blast radius of the incident.

You are provided with two files:
1. `/home/user/employees.csv`: A relational table of our employees containing `emp_id`, `manager_id` (the ID of their direct manager, empty if they have no manager), and `name`.
2. `/home/user/access_logs.json`: A document-oriented log of system accesses containing a list of JSON objects, each with `emp_id`, `system_name`, and `access_time` (ISO-8601 format).

The suspect manager has the employee ID `MGR-042`. 

Please write a Python script at `/home/user/audit_report.py` that does the following:
1. Ingests the CSV and JSON data.
2. Performs a recursive/hierarchical resolution to identify `MGR-042` and ALL of their direct and indirect subordinates (the entire sub-tree in the management hierarchy).
3. Cross-references this cohort's `emp_id`s with the document-based access logs.
4. Uses analytical aggregations to calculate the following for each system accessed by anyone in this specific cohort:
   - `total_accesses`: The total number of times the system was accessed by members of the cohort.
   - `latest_access`: The most recent `access_time` for that system by any member of the cohort.
5. Exports this materialized view to a CSV file at `/home/user/audit_results.csv`.

The output CSV `/home/user/audit_results.csv` must:
- Have exactly the columns: `system_name,total_accesses,latest_access`
- Be sorted by `total_accesses` in descending order. If there is a tie, sort by `system_name` in ascending alphabetical order.
- Not include accesses from employees outside of `MGR-042`'s management hierarchy.

Run your script to ensure the output file is generated correctly. Do not use any external databases; you may use standard Python libraries (like `sqlite3` for in-memory processing, `json`, `csv`, etc.).