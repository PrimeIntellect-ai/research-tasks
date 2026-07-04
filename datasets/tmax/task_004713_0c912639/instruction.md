As a compliance officer, I need to audit our company's expense database to identify potentially anomalous spending. I have an SQLite database located at `/home/user/expenses.db`.

Your task is to write a Python script `/home/user/audit.py` that processes this data and flags suspicious expenses. 

The database has the following schema:
- `departments` (id INTEGER PRIMARY KEY, name TEXT)
- `categories` (id INTEGER PRIMARY KEY, name TEXT)
- `employees` (id INTEGER PRIMARY KEY, name TEXT, role TEXT, department_id INTEGER)
- `expenses` (id INTEGER PRIMARY KEY, emp_id INTEGER, cat_id INTEGER, amount REAL, date TEXT)

A suspicious expense is defined as any expense whose `amount` is **strictly greater** than the overall average amount of all expenses in that exact same `category` across the entire company.

Your script must:
1. Accept exactly one command-line argument: the name of a department (e.g., `python /home/user/audit.py "Sales"`).
2. Connect to `/home/user/expenses.db`.
3. Use a parameterized SQL query featuring complex joins and a subquery (or CTE) to find all suspicious expenses for employees in the specified department.
4. Export the results to a JSON file at `/home/user/audit_report.json`.

The output JSON must be a list of objects, sorted by `date` ascending, and then by `amount` descending. Each object must have the following exact keys:
- `"employee_name"` (string)
- `"department"` (string)
- `"category"` (string)
- `"amount"` (float)
- `"category_average"` (float, strictly rounded to 2 decimal places)
- `"date"` (string, YYYY-MM-DD)

After writing the script, execute it for the `"Sales"` department to generate the final `audit_report.json`.

**Constraints:**
- Do not use ORMs (like SQLAlchemy). Use the built-in `sqlite3` module.
- The average must be calculated securely within the database query, not in Python memory.
- Prevent SQL injection by correctly parameterizing the department name.