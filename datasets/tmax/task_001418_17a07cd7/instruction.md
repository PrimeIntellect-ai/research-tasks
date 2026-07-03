You are a Database Reliability Engineer handling an incident. An SQLite database backup (`/home/user/backup.db`) contains critical employee data, but we suspect the index on the `status` column (`idx_status`) is corrupted, leading to stale or missing rows when queried standardly. 

Your task is to extract the active employee data safely, perform an aggregation (similar to a NoSQL aggregation pipeline), and map the result to a JSON document structure.

Requirements:
1. Write a C program at `/home/user/process_backup.c` that connects to `/home/user/backup.db`.
2. The database contains a table: `employees (id INTEGER, name TEXT, region TEXT, salary INTEGER, status TEXT)`.
3. Use a parameterized query to fetch employees where `status = ?` (bind the value `"ACTIVE"` to the parameter).
4. **Crucial:** You must explicitly bypass the corrupted index by using SQLite's `NOT INDEXED` clause in your `SELECT` statement.
5. In your C program, process the retrieved rows to aggregate the total salary per `region` (mimicking a NoSQL `$group` pipeline step). 
6. Output the aggregated data to a file at `/home/user/region_salaries.json`. The output must be a well-formatted JSON array of objects, mapped exactly like this:
   ```json
   [
     {"region": "EU", "total_salary": 250000},
     {"region": "NA", "total_salary": 320000}
   ]
   ```
7. The JSON array must be sorted alphabetically by the `region` string.
8. Compile your program to `/home/user/process_backup` and execute it so that the JSON file is created. Link against the standard sqlite3 library (`-lsqlite3`).

Ensure your final JSON output is perfectly formatted as standard JSON.