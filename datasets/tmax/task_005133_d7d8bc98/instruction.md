You are a compliance officer auditing an organization's IT system access. You have been provided with an SQLite database located at `/home/user/audit.db`. The database contains undocumented tables related to employees, systems, and direct system access.

Your objective is to identify "Conflict of Interest" (CoI) violations based on the organizational hierarchy. 

A CoI violation occurs when an employee has access to BOTH the Trading system (System ID: 101) AND the Auditing system (System ID: 202). 
Crucially, an employee's access is the union of their direct access AND the access of all their subordinates (direct and indirect, traversing down the management hierarchy). For example, if Alice manages Bob, and Bob manages Charlie, Alice has access to all systems that she, Bob, and Charlie have direct access to.

You must write a Python script `/home/user/audit_coi.py` that performs the following tasks:
1. Reverse engineers the database schema to understand the tables for employees, systems, and access. (You will need to explore `/home/user/audit.db` yourself).
2. Uses recursive/hierarchical SQL queries (e.g., Recursive CTEs) to resolve the full access graph for every employee.
3. Identifies all employees who have a CoI violation.
4. Generates a CSV report at `/home/user/coi_report.csv` containing the `emp_id` and `department` of all employees with a CoI violation. The CSV must have headers `emp_id,department` and be sorted by `emp_id` in ascending order.
5. Uses SQL Window Functions to generate a second CSV report at `/home/user/dept_stats.csv`. This report must list every department that has AT LEAST ONE CoI violation, the total number of CoI violations in that department, and the rank of the department based on the number of CoI violations (using the `RANK()` function, descending order of violations). If there is a tie in rank, order alphabetically by department name. The headers must be `department,coi_count,dept_rank`.

Ensure your Python script relies on SQLite to do the heavy lifting (recursive CTEs and window functions) rather than doing the data processing in Python. 

Run your script to produce the two CSV files. The automated test will verify the contents of `/home/user/coi_report.csv` and `/home/user/dept_stats.csv`.