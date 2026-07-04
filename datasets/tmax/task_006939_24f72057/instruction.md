You are a database administrator tasked with optimizing and extracting hierarchical data for a new NoSQL document store. 

We have an existing SQLite database located at `/home/user/company.db` containing an `employees` table with the following schema:
`CREATE TABLE employees (id INTEGER PRIMARY KEY, name TEXT, manager_id INTEGER, salary REAL);`

Your task is to write a C program at `/home/user/export_hierarchy.c` that does the following:
1. Connects to the SQLite database at `/home/user/company.db`.
2. Uses a recursive SQL query (CTE) to calculate the "total department salary" for each employee. An employee's total department salary is their own salary plus the salaries of all their direct and indirect reports (recursive).
3. Cross-maps this relational result into a JSON array of documents.
4. Exports the resulting JSON array to `/home/user/salary_rollup.json`.

The JSON file must be strictly formatted as a single JSON array of objects, sorted by `id` in ascending order. Each object should have the exact keys `id` (integer), `name` (string), and `total_salary` (float/real formatted to 2 decimal places).
Example format for `/home/user/salary_rollup.json`:
```json
[
  {"id": 1, "name": "Alice", "total_salary": 465000.00},
  {"id": 2, "name": "Bob", "total_salary": 205000.00}
]
```

Compile your program using:
`gcc -o /home/user/export_hierarchy /home/user/export_hierarchy.c -lsqlite3`

Execute the program so that `/home/user/salary_rollup.json` is generated. You may install any necessary C development libraries using your package manager if they are not present.