You are an AI assistant helping a data engineer build a lightweight, embedded ETL processing step. 

We have a raw dataset of e-commerce telemetry logs at `/home/user/raw_events.csv`. The CSV has no header and contains the following columns:
`timestamp` (TEXT), `user_id` (INTEGER), `event_type` (TEXT), and `item_price` (REAL).

Your task is to write a C program that ingests this data into an SQLite database, optimizes the schema for a specific analytical query, and executes the query with pagination to produce a final report.

Perform the following steps:
1. If necessary, install the SQLite3 development libraries (`libsqlite3-dev`) via your package manager to allow compiling against SQLite.
2. Write a C program at `/home/user/etl_processor.c`.
3. The C program must:
   - Create (or open) an SQLite database named `/home/user/analytics.db`.
   - Create a table named `events` with the schema: `timestamp TEXT, user_id INTEGER, event_type TEXT, item_price REAL`.
   - Read the `/home/user/raw_events.csv` file and insert all rows into the `events` table. Use prepared statements and transactions to ensure it processes efficiently.
   - Design and execute a `CREATE INDEX` statement to create an index named `idx_performance` that optimizes querying by `event_type` while aggregating `item_price` grouped by `user_id`.
   - Execute a query to find the total amount spent (`SUM(item_price)`) per `user_id`, filtered strictly to rows where `event_type` is exactly `'purchase'`. 
   - The results must be sorted by the total amount spent in **descending** order.
   - Apply pagination to the result: we only want the **second page** of results, assuming a page size of 5 (i.e., skip the top 5 spenders and retrieve the next 5).
   - Write these 5 results to `/home/user/report.out`, with exactly one line per row in the format: `User <user_id> spent <total_spent_rounded_to_2_decimal_places>` (e.g., `User 42 spent 150.50`).
4. Compile your program to `/home/user/etl_processor` using `gcc`.
5. Run `./etl_processor` so that `analytics.db` and `report.out` are generated.

Do not write any bash scripts to process the CSV—the ETL logic and database operations must be entirely handled within the compiled C program using the SQLite C API (`sqlite3.h`).