You are a database administrator tasked with writing an optimized data retrieval tool in C for a custom company application. 

A SQLite database is located at `/home/user/company.db` with the following schema:

```sql
CREATE TABLE departments (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE employees (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    department_id INTEGER NOT NULL,
    manager_id INTEGER,
    salary REAL NOT NULL,
    FOREIGN KEY(department_id) REFERENCES departments(id),
    FOREIGN KEY(manager_id) REFERENCES employees(id)
);
```

Your task is to write a C program at `/home/user/query.c` that connects to this SQLite database and performs a complex hierarchical query using the SQLite C API (`sqlite3.h`). 

The query must:
1. Use a **Recursive CTE** to traverse the employee hierarchy top-down, starting from the CEO (the employee where `manager_id IS NULL`). The CEO is at hierarchy level 0, their direct reports are at level 1, and so on.
2. Join the results with the `departments` table to fetch the department name for each employee.
3. Sort the results first by `level` (Ascending) and then by `salary` (Descending).
4. Apply pagination to the results: retrieve exactly 4 rows, skipping the first 3 rows (i.e., `LIMIT 4 OFFSET 3`).

The C program must execute this query and write the result rows to a CSV file located at `/home/user/results.csv`.
The CSV file should not have a header, and the columns must be strictly ordered as follows:
`employee_id,name,department_name,level,salary`
Format the salary to exactly 2 decimal places (e.g., `120000.00`).

Compile your C program using `gcc /home/user/query.c -lsqlite3 -o /home/user/query`, and then execute it so the `/home/user/results.csv` file is generated.