You are a systems engineer called in to investigate a memory leak in a critical long-running binary service. The service recently crashed and was OOM (Out Of Memory) killed. Unfortunately, the source code for this service was lost during a recent migration, and all we have left is the compiled binary and its database.

The system is located in `/home/user/app/`.
Inside this directory, you will find:
1. `service_bin`: The compiled Linux binary of the service.
2. `data.db`: An SQLite3 database used by the service. Because the service crashed, the database was left in an inconsistent state, and uncommitted data remains in its WAL (Write-Ahead Log) file.

Your objectives are to recover the data, reverse engineer the binary to understand its behavior, and extract the corrupted state:

1. **Database Recovery**: Checkpoint the Write-Ahead Log (`-wal` file) into the main `data.db` database so that all recent inserts are fully recovered and visible to standard queries.
2. **Binary Reverse Engineering (Leak Identification)**: Analyze `service_bin` to find the exact name of the C/C++ function responsible for the memory leak. The original developer noted that the function name explicitly describes the bug (e.g., it contains words like "alloc", "leak", or "unfreed"). Write the exact function name to `/home/user/report/leak_func.txt`.
3. **Binary Reverse Engineering (Query Extraction)**: Extract the hardcoded SQL query from the binary. The service uses a specific `SELECT` query to fetch high-load metrics from the database just before it leaks memory. 
4. **Query Execution**: Run the exact SQL query you extracted from the binary against the recovered `data.db`. Export the results to a CSV file at `/home/user/report/query_out.csv` (without headers, comma-separated).

Constraints:
- You must create the `/home/user/report/` directory if it does not exist.
- Use standard Linux tools (like `strings`, `objdump`, `nm`, `gdb`, `sqlite3`) to complete the task.