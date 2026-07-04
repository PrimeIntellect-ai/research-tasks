You are a database administrator tasked with fixing and optimizing a custom C utility used to query a graph database stored in SQLite. 

The file `/home/user/company.db` is a SQLite database containing a single table representing an organizational hierarchy:
`CREATE TABLE employees (id INTEGER PRIMARY KEY, name TEXT, manager_id INTEGER);`

There is a C program located at `/home/user/export_hierarchy.c` that is supposed to retrieve an employee and all their direct and indirect subordinates (a recursive graph query) and export the results to standard output in CSV format (`id,name`). 

However, the program currently has several issues:
1. **Wrong Results / Implicit Cross Join:** The recursive CTE (Common Table Expression) inside the C code contains a logic error. In the recursive step, it performs an implicit cross join by selecting from `employees e, subordinates s` without a connecting condition, causing an infinite loop or Cartesian explosion.
2. **Missing Parameterization:** The program fails to securely bind the target employee ID (passed as a command-line argument) to the prepared statement. 
3. **Missing Index:** The query is slow on large datasets because the database lacks an appropriate index for looking up subordinates.

Your task is to:
1. Modify `/home/user/export_hierarchy.c` to fix the recursive SQL query so it correctly traverses the hierarchy (i.e., joining where the employee's `manager_id` equals the subordinate's `id`).
2. Implement proper parameterized query construction in the C code using `sqlite3_bind_int` to bind the employee ID from `argv[1]` to the query, instead of string concatenation or hardcoded values.
3. Write a SQL script at `/home/user/optimize.sql` that creates an index named `idx_manager` on the `manager_id` column of the `employees` table. Apply this script to `/home/user/company.db`.
4. Compile the C program: `gcc /home/user/export_hierarchy.c -o /home/user/export_hierarchy -lsqlite3` (Install `libsqlite3-dev` via apt if necessary).
5. Execute the compiled program for employee ID `1` and save the output exactly to `/home/user/reports_1.csv`.

The output CSV `/home/user/reports_1.csv` should contain no headers, just the `id,name` of employee 1 and all their recursive subordinates, one per line.