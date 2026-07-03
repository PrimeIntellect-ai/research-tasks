You are a database administrator tasked with optimizing a poorly written C++ data retrieval tool. 

In `/home/user/`, you will find an SQLite database named `retail.db` and a C++ source file `report.cpp`.
Currently, `report.cpp` is extremely inefficient. It connects to the database, takes a city name as a command-line argument, and calculates the top 3 users by total purchase amount in that city. However, it does this by fetching *all* rows and doing the filtering and aggregation in C++ memory, which is slow and memory-intensive.

Your task:
1. Reverse engineer the schema of `retail.db` to understand the relationships between the tables.
2. Rewrite `report.cpp` to perform the filtering, joining, and aggregation entirely within a single, optimized SQL query using `JOIN`, `GROUP BY`, `ORDER BY`, and `LIMIT`.
3. The SQL query inside `report.cpp` MUST use parameterized queries (prepared statements with `sqlite3_bind_*`) to prevent SQL injection for the city name argument.
4. Analyze the new query plan and create any necessary indexes in `retail.db` directly using the `sqlite3` CLI to optimize the new query (e.g., an index that helps with the join or filtering).
5. Compile your modified `report.cpp` into an executable named `/home/user/report` (make sure to link the `sqlite3` library).
6. Run your compiled program for the city `"Seattle"` and redirect its standard output to `/home/user/report_output.txt`.

The output format printed by your C++ program (and captured in `report_output.txt`) must be exactly 3 lines, formatted as:
`<user_name>|<total_amount>`
Where `<total_amount>` is formatted to 2 decimal places.

Ensure `/home/user/report_output.txt` is created with the correct results.