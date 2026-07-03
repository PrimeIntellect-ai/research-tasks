As a data analyst, you need to process a list of users and extract their event counts from an SQLite database. 

You are provided with:
- An SQLite database at `/home/user/data.db`
- An input CSV at `/home/user/input.csv` containing a list of `user_id`s.

Unfortunately, the database has experienced partial storage corruption. Specifically, an index used for querying user events is corrupted. Any standard query that attempts to use this index will result in a "database disk image is malformed" error. You are **not allowed** to modify the database file (e.g., no `DROP INDEX`, no `REINDEX`, no writing to the file).

Your task:
1. Reverse engineer the schema of the database to understand the tables and columns.
2. Write a C program at `/home/user/process.c` that reads `user_id`s from `/home/user/input.csv`.
3. For each `user_id`, query the database to find the count of `'login'` events and `'purchase'` events. You must structure your SQL queries to bypass the corrupted index (forcing a table scan) without modifying the database schema.
4. Output the results to a file named `/home/user/output.csv` with the exact header `user_id,login_count,purchase_count` and the corresponding counts for each user in the input file.
5. Compile your C program to `/home/user/process` and execute it to generate the final `output.csv`.

Requirements:
- You must write the solution in C using the standard SQLite3 C API (`sqlite3.h`).
- The output CSV must accurately reflect the data in the uncorrupted main table.
- Do not modify or copy the `data.db` file. Query it directly in its current state.