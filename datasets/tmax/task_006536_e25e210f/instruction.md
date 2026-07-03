You are a database administrator tasked with writing a C program to efficiently query a hierarchical employee structure from a SQLite database. 

A database file exists at `/home/user/company.db` with a single table `employees`:
- `emp_id` (INTEGER PRIMARY KEY)
- `emp_name` (TEXT)
- `manager_id` (INTEGER) - references `emp_id` of the employee's manager (NULL for the CEO)

Your task is to write a C program located at `/home/user/get_org.c` that does the following:
1. Takes a single integer command-line argument representing the root `emp_id`.
2. Connects to `/home/user/company.db` using the SQLite3 C API.
3. Uses a **parameterized** Recursive Common Table Expression (CTE) query to fetch the given employee and all of their direct and indirect subordinates.
4. The query must calculate the "depth" of each employee relative to the queried root (the root employee has depth 0, direct reports depth 1, etc.).
5. Orders the result by `depth` ascending, then by `emp_id` ascending.
6. Writes the results to `/home/user/org_report.txt`.

The output format in `/home/user/org_report.txt` must be exactly:
```
<depth> - <emp_id>: <emp_name>
```
(One employee per line).

After writing the code, compile it into an executable named `/home/user/get_org` (remember to link the sqlite3 library).
Finally, execute your program to generate the report for the employee with `emp_id` = 2. 

Make sure the final report is generated at `/home/user/org_report.txt`.