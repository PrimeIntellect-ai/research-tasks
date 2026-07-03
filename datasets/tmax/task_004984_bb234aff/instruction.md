You are a Database Reliability Engineer (DBRE) investigating a performance bottleneck in our daily backup verification pipeline. 

We have a stripped binary located at `/app/chunk_verifier` that takes the path to a SQLite database as an argument. The database (`/home/user/backup_metadata.db`) contains backup chunk metadata with two tables:
1. `chunks` (`id` INTEGER PRIMARY KEY, `size` INTEGER, `timestamp` DATETIME)
2. `chunk_dependencies` (`parent_id` INTEGER, `child_id` INTEGER)

The `/app/chunk_verifier` binary materializes the dependency graph of backup chunks, computes the rolling cumulative size of chunks per dependency chain using window functions, and outputs a single integer: the maximum cumulative backup chain size.

Unfortunately, the binary is terribly slow. Your task is to:
1. Reverse-engineer or observe the binary's behavior to understand the exact metric it calculates.
2. Write a Python script at `/home/user/fast_verifier.py` that connects to `/home/user/backup_metadata.db` using the `sqlite3` module.
3. Construct an optimized parameterized SQL query (using CTEs for graph projection and window functions for analytical aggregation) to compute the exact same integer result.
4. Print only this integer to standard output.

Your Python script must chain the query execution directly to standard output and complete significantly faster than the binary. 

Requirements:
- Output must be exactly the integer result, followed by a newline.
- Your script's execution time will be measured against the binary. It must achieve a speedup of at least 5.0x.