You are a database administrator troubleshooting a critical issue. An SQLite database `/home/user/telemetry.db` containing network edge connections has a corrupted B-Tree index on its timestamp column. Running standard queries that rely on the optimizer often returns stale or skipped rows. 

To safely bypass the database engine's corrupted query planner and extract crucial network patterns, you must write a standalone C program that extracts the raw data and performs the necessary analytical processing and pattern matching.

Write a C program at `/home/user/extractor.c` that connects to `/home/user/telemetry.db` and performs the following result processing:

1. Connects to the database and queries the `signals` table. The table schema is: `(id INTEGER PRIMARY KEY, source TEXT, destination TEXT, power REAL, timestamp INTEGER)`. 
2. Ensure your query forces a full table scan and does NOT use any indexes. (Hint: In SQLite, applying a unary `+` to a column name in a WHERE or ORDER BY clause, or avoiding ORDER BY in SQL and doing it in C, bypasses indexes).
3. Performs Knowledge Graph Pattern Matching in C (or via a carefully crafted SQL query that avoids the index) to find all valid "relay paths" (A -> B -> C). A valid relay path is defined as:
   - A connection from `source` A to `destination` B with `power` > 50.0
   - A subsequent connection from `source` B to `destination` C with `power` > 50.0
   - The `timestamp` of the B->C connection must be strictly greater than the A->B connection, but by no more than 100 seconds (i.e., `0 < timestamp2 - timestamp1 <= 100`).
4. Computes the `path_power` for each relay path, defined as the minimum of the two connection powers.
5. Exports the results to a CSV file at `/home/user/valid_relays.csv` with the exact header: `start,relay,end,path_power`.
6. Sort the CSV output primarily by `path_power` DESCENDING, and secondarily by the `start` node name ASCENDING. Format `path_power` to exactly one decimal place.

Compile your program using `gcc /home/user/extractor.c -o /home/user/extractor -lsqlite3` and execute it to generate the CSV.