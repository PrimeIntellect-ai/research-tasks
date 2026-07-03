You are a database administrator tasked with optimizing and processing queries for an undocumented e-commerce system. 

You have been provided with an SQLite database file at `/home/user/ecommerce.db`. Your goal is to reverse-engineer the data model, optimize a specific analytical query by creating appropriate indexes, and write a C++ program to process the results.

Please perform the following steps:
1. Analyze the schema of `/home/user/ecommerce.db` to understand how clients, their shopping carts, cart items, and products are linked.
2. Write a C++ program at `/home/user/process.cpp`. The program must use the SQLite3 C API (`<sqlite3.h>`) and accept two command-line arguments representing a date range (start_date and end_date in `YYYY-MM-DD` format).
3. When executed, your C++ program must:
   - Create any necessary indexes to optimize querying the total spend per client within a specific date range based on checkout dates.
   - Construct a **parameterized query** to find the top 5 clients by total spend (sum of `quantity * price`) whose carts were checked out strictly between the start_date and end_date (inclusive).
   - Run `EXPLAIN QUERY PLAN` on your parameterized query and write the exact output rows (the `detail` column) to `/home/user/query_plan.txt`, one step per line.
   - Execute the actual parameterized query and write the results to `/home/user/top_clients.csv`. The CSV should have no header, and each line should be formatted as `client_id,total_spend`. The `total_spend` must be formatted to exactly 2 decimal places.

Compile your program using:
`g++ /home/user/process.cpp -lsqlite3 -o /home/user/process`

Ensure that running `./process 2023-01-01 2023-12-31` successfully creates the optimized indexes, dumps the query plan, and writes the correct aggregated results.

Note:
- You must use SQLite's C API (`sqlite3_prepare_v2`, `sqlite3_bind_text`, etc.).
- Ensure your program handles the database connection and file I/O properly.