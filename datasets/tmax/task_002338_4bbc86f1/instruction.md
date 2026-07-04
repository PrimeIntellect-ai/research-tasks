You are assisting a compliance officer auditing a company's internal authorization system. The system uses role-based access control (RBAC) where roles can inherit permissions from other roles recursively.

There is a Python script located at `/home/user/audit_report.py` that queries the SQLite database `/home/user/audit.db`. The script is supposed to find all employees who have "SuperAdmin" privileges, either directly or through recursive role inheritance. However, the current script contains a flawed SQL query with an implicit cross join, causing it to return incorrect results (mostly false positives).

Database Schema:
- `employees` (id INTEGER PRIMARY KEY, name TEXT)
- `roles` (role_id INTEGER PRIMARY KEY, role_name TEXT)
- `role_hierarchy` (role_id INTEGER, inherits_role_id INTEGER) -- 'role_id' inherits all permissions of 'inherits_role_id'
- `employee_roles` (emp_id INTEGER, role_id INTEGER)

Your task:
1. Fix the SQL query in `/home/user/audit_report.py`. You must use a Recursive CTE to traverse the `role_hierarchy` graph to find all roles that inherit the 'SuperAdmin' role (recursively), and then properly join this with the `employees` and `employee_roles` tables to find the assigned employees.
2. The script must output the valid, audited employees to `/home/user/admin_audit.json` in the following exact JSON format (a list of dictionaries, ordered by `emp_id` ascending):
```json
[
  {
    "emp_id": 101,
    "name": "Alice"
  }
]
```

Do not modify the database schema. Update the Python script so that it runs successfully and generates the correct JSON file.