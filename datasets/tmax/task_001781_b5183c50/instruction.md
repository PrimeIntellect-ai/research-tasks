You are a data engineer responsible for modernizing our ETL pipelines. We currently rely on a legacy, undocumented binary tool located at `/app/query_oracle` to extract anomaly reports from our SQLite databases. We need to integrate this extraction logic directly into our new C-based pipeline.

Your task is to reverse-engineer the behavior of the `/app/query_oracle` binary and reimplement it entirely in C. 

The binary takes a single command-line argument: the path to a SQLite database.
The databases processed by this tool always have the following schema:
```sql
CREATE TABLE sensors (id INTEGER PRIMARY KEY, name TEXT, category TEXT);
CREATE TABLE events (id INTEGER PRIMARY KEY, sensor_id INTEGER, ts INTEGER, metric REAL);
```

The tool performs a complex query involving joins and analytical window functions (computing rolling aggregates), flags certain records as anomalies based on a threshold, and exports the results to standard output in a specific CSV format. 

You must:
1. Analyze the `/app/query_oracle` binary to understand its exact filtering, aggregation, and formatting logic. You can generate sample SQLite databases to observe its inputs and outputs, or reverse-engineer the binary directly.
2. Write a C program at `/home/user/solution.c` that uses `libsqlite3` to perform the exact same data querying and result processing.
3. Compile your program to `/home/user/solution` (e.g., `gcc -O2 solution.c -lsqlite3 -o solution`).
4. Ensure your compiled program takes the database path as its first argument and produces BIT-EXACT identical output to `/app/query_oracle` for ANY database adhering to the schema. 

Your solution will be tested against randomly generated databases to ensure perfect equivalence with the oracle.