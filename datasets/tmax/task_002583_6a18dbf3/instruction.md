You are a database administrator tasked with optimizing a data processing pipeline. We have a set of raw CSV files representing a corporate hierarchy and sales records. The previous pipeline was too slow, so we are migrating to a custom C++ solution using SQLite to process the data efficiently.

Your task is to write a C++ program that ingests this data, creates an optimized database schema with appropriate indexes, performs a complex analytical query, and writes the results to a file.

Since you do not have root access to install libraries, you must download the SQLite amalgamation source and compile it directly with your C++ code.

**Step 1: Environment Setup**
1. Download the SQLite amalgamation source code (version 3.44.0 or similar) into `/home/user/sqlite/`.
   URL: `https://www.sqlite.org/2023/sqlite-amalgamation-3440000.zip` (You can use `wget` and `unzip`).

**Step 2: Database and Schema Setup**
Write a C++ program at `/home/user/report_generator.cpp`. The program must create a local SQLite database file named `/home/user/company.db` and create the following tables:
- `departments` (id INTEGER PRIMARY KEY, name TEXT)
- `employees` (id INTEGER PRIMARY KEY, name TEXT, department_id INTEGER, manager_id INTEGER)
- `sales` (id INTEGER PRIMARY KEY, employee_id INTEGER, amount INTEGER)

**Step 3: Data Ingestion and Optimization**
Your C++ program should read the following CSV files (which already exist) and insert the data into the tables:
- `/home/user/data/departments.csv`
- `/home/user/data/employees.csv`
- `/home/user/data/sales.csv`

To optimize the queries, your program MUST explicitly execute SQL commands to create at least two indexes:
1. An index on `employees(department_id)`
2. An index on `sales(employee_id)`

**Step 4: Analytical Query**
Using the SQLite C API, execute a single complex SQL query that:
1. Uses a **Recursive CTE** (Graph Projection) to find the "Top Manager" for every employee. The Top Manager is the employee at the top of the management chain (where `manager_id` is NULL).
2. Uses **Window Functions** to calculate the total sales for each employee and their rank within their department based on total sales (highest sales = rank 1).
3. **Joins** these results with the `departments` table.
4. **Filters** to only include employees who have at least one sale.
5. **Sorts** the final results by `Department Name` (ASC), then by `Department Rank` (ASC).

**Step 5: Output Generation**
Write the results to `/home/user/report.txt` in exactly this format for each row:
`EmployeeName | DepartmentName | TopManagerName | TotalSales | DeptRank`

Compile your C++ program using `g++` (e.g., `g++ report_generator.cpp sqlite/sqlite3.c -o report_generator -I./sqlite -lpthread -ldl`) and run it to generate the report.