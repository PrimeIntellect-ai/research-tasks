You are a data engineer building a new C++ ETL pipeline. We have an SQLite database located at `/app/data.db` containing three tables: `users`, `sessions`, and `orders`.

Our previous pipeline was producing incorrect aggregations because it joined `orders` and `sessions` on `user_id` alone, resulting in an implicit cross join for users with multiple sessions. The correct data model and temporal relationship constraints are documented in an architecture diagram located at `/app/schema.png`.

Your task:
1. Analyze `/app/schema.png` to reverse-engineer the correct data model and join conditions.
2. Write a C++ program at `/home/user/etl.cpp` that connects to `/app/data.db` using the SQLite C API (`sqlite3.h`).
3. Your C++ program must execute a query using the correct relationships to calculate the total order amount for each `session_id`.
4. Output the results to `/home/user/summary.csv` with the header `session_id,total_amount` (with total_amount formatted to 2 decimal places).
5. Compile your program to `/home/user/etl_bin` using `g++` and link the sqlite3 library (`-lsqlite3`).

You may install any necessary packages (like `sqlite3`, `libsqlite3-dev`, `tesseract-ocr`) to inspect the database and the image. Execute your compiled program so that `/home/user/summary.csv` is generated.