You are a data engineer building a lightweight ETL pipeline using Bash and SQLite. 

Your task is to write a parameterized Bash script that extracts a hierarchical organizational chart from an SQLite database, filters and paginates the results, and exports them as a JSON array.

The database is located at `/home/user/company.db` and contains a single table:
`employees(id INTEGER PRIMARY KEY, name TEXT, manager_id INTEGER, salary INTEGER, department TEXT)`

Create a Bash script at `/home/user/extract_hierarchy.sh` that takes exactly three positional arguments:
1. `MANAGER_ID` (integer)
2. `MIN_SALARY` (integer)
3. `LIMIT` (integer)

The script must perform the following:
1. Connect to `/home/user/company.db`.
2. Use a recursive SQL query (CTE) to find the employee with `id = MANAGER_ID` and all of their direct and indirect subordinates (the entire subtree).
3. Filter the resulting hierarchy to only include employees (including the root manager, if applicable) whose `salary` is greater than or equal to `MIN_SALARY`.
4. Sort the filtered results first by `salary` in descending order, and then by `id` in ascending order to break ties.
5. Limit the output to at most `LIMIT` rows.
6. Export and print the final result to standard output strictly as a JSON array of objects. Each object must have exactly three keys: `id`, `name`, and `salary`. 
7. Make sure the script is executable (`chmod +x`).

Example of expected output format printed to stdout:
```json
[
  {"id": 4, "name": "Alice", "salary": 95000},
  {"id": 7, "name": "Bob", "salary": 80000}
]
```

Do not include any extra text, logging, or markdown formatting in the standard output of the script—only the valid JSON array.