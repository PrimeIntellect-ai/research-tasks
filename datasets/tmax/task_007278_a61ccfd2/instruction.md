You are a data engineer building ETL pipelines. We need to process sales data from a SQLite database and extract a specific departmental report using C++.

A SQLite database is located at `/home/user/company.db`. It contains two tables:
1. `employees` (id INTEGER PRIMARY KEY, name TEXT, manager_id INTEGER) - represents the organizational hierarchy.
2. `sales` (id INTEGER PRIMARY KEY, employee_id INTEGER, sale_date TEXT, amount REAL) - represents daily sales by employees.

Your task:
Write a C++ program (e.g., `/home/user/process.cpp`) that connects to `/home/user/company.db` using the SQLite3 C API (`sqlite3.h`). 
The program must execute a single query that:
1. Uses a Recursive CTE to find employee ID 1 and all of their direct and indirect subordinates in the hierarchy.
2. Aggregates the total sales amount for this specific group of employees per `sale_date`.
3. Uses a Window Function to calculate the 3-day rolling average of these daily total sales (the current day and up to 2 preceding days of sales data).

The C++ program must execute this query and write the results to `/home/user/report.csv`. 
The CSV must have the exact header: `date,daily_total,rolling_avg`.
The `rolling_avg` must be rounded to exactly 2 decimal places (e.g., `250.00`, `183.33`).

Constraints:
- Use only standard C++ libraries and the SQLite3 C API (`sqlite3.h`).
- The C++ compilation command should be standard, such as `g++ process.cpp -lsqlite3 -o process`.
- You must write the code, compile it, and run it to produce `/home/user/report.csv`.
- Make sure to ignore sales from employees not in the hierarchy of employee 1.