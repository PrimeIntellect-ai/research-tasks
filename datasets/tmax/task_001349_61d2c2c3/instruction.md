You are an AI assistant helping a compliance officer audit an organization's financial transactions. 

The company stores its organizational hierarchy and financial transactions in a SQLite database located at `/home/user/audit.db`. 

Your task is to write a C++ program that identifies suspicious transactions based on department baselines and traces the accountability up the corporate hierarchy.

Here are your instructions:
1. Install any necessary system packages to compile and link C++ programs with SQLite3.
2. Write a C++ program at `/home/user/auditor.cpp`. The program must connect to `/home/user/audit.db`.
3. The database contains two tables:
   - `employees (emp_id INTEGER PRIMARY KEY, name TEXT, manager_id INTEGER, department TEXT)`: `manager_id` references `emp_id`. The top-level executive has `manager_id = NULL`.
   - `transactions (tx_id INTEGER PRIMARY KEY, emp_id INTEGER, amount REAL, tx_date TEXT)`
4. The C++ program must execute queries (using window functions and recursive queries) to identify "suspicious" transactions. A transaction is defined as suspicious if its `amount` is strictly greater than `3.0` times the average transaction amount of ALL transactions within that employee's `department`.
5. For each suspicious transaction, use a recursive hierarchical query to trace the employee's management chain all the way to the top-level manager (the employee with a `NULL` manager).
6. The C++ program must output a CSV file at `/home/user/audit_report.csv` containing the suspicious transactions.
   - The CSV must have exactly this header: `tx_id,emp_name,amount,top_manager_name`
   - The rows must be ordered by `tx_id` ascending.
   - Output amounts formatted to one decimal place if they are whole numbers (e.g., `1500.0`).
7. Compile your program to `/home/user/auditor` and execute it to generate the CSV.

Ensure your code handles the database connection safely and handles potential errors gracefully. Do not modify the database contents.