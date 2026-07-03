You are acting as a compliance officer auditing an organization's internal access control system. Your objective is to identify all employees who have transitive access to highly sensitive resources through nested group memberships. 

The system's access control data is stored in a SQLite database located at `/home/user/audit.db`. 

The database contains the following tables:
- `employees` (`emp_id` INT, `name` TEXT)
- `groups` (`group_id` INT, `parent_group_id` INT, `name` TEXT) - Note: `parent_group_id` is NULL for top-level groups. A group inherits all access permissions of its parent group.
- `group_members` (`emp_id` INT, `group_id` INT)
- `permissions` (`group_id` INT, `resource_name` TEXT)

Your task consists of three parts:

1. **Python Data Extractor (`/home/user/audit_query.py`)**
Write a Python script that takes a single command-line argument: the `resource_name`.
The script must connect to `/home/user/audit.db` and execute a **parameterized query** that uses a **Recursive CTE** to traverse the `groups` hierarchy. It must find all employees who have access to the provided `resource_name`. An employee has access if they are a member of a group that has direct permission to the resource, OR if they are a member of a group that is a descendant (child, grandchild, etc.) of a group with direct permission. 
The script should output the matching records to standard output in tab-separated format (`emp_id\tname`), sorted numerically by `emp_id`.

2. **Reporting Pipeline (`/home/user/generate_report.sh`)**
Write a bash script that executes your Python script, passing `"CONFIDENTIAL_FINANCE_RECORDS"` as the parameter.
The bash script must capture the output and format it into a CSV file saved at `/home/user/unauthorized_access.csv`. The CSV file must include a header row: `ID,Name`.

3. **Execution**
Run your bash script to generate the final CSV report.

Ensure that:
- The recursive CTE accurately models the top-down inheritance (if Group A has access, and Group B's parent is Group A, then Group B also has access. An employee in Group B therefore has access).
- You do not use hardcoded string concatenation for the resource name in your SQL query; use proper parameter binding to prevent SQL injection.