You are a Database Reliability Engineer. We have a backup dependency system stored in an SQLite database at `/home/user/backup_graph.db`. Recently, our automated backup scripts started failing because they were querying a materialized cache table (`stale_routes_cache`) that has become corrupted and returns stale, circular dependency rows. 

Your task is to write a C program that connects to this database, bypasses the corrupted cache by analyzing the raw schema, builds a proper index to optimize graph traversal, and uses a Recursive Common Table Expression (CTE) to determine the correct backup order.

Here are the requirements:
1. Examine the SQLite database `/home/user/backup_graph.db`. You will find the raw base tables representing the servers and their backup dependencies (which server must be backed up before another).
2. Write a C program at `/home/user/resolver.c` using the SQLite3 C API (`sqlite3.h`). 
3. Your C program must:
   - Connect to `/home/user/backup_graph.db`.
   - Execute a SQL command to create an optimal index on the raw dependency table to ensure the recursive graph pattern matching query runs efficiently.
   - Execute a Recursive CTE query that calculates the "backup phase" (or depth) for each server. Servers with NO dependencies are in Phase 0. Servers that depend only on Phase 0 servers are in Phase 1, and so on.
   - Output the results to `/home/user/backup_plan.log` in exactly the following format (sorted by Phase ascending, then hostname ascending):
     `Phase 0: db-primary`
     `Phase 1: db-replica, app-server-1`
     (Wait, note that it should be one server per line to make formatting easier, like `Phase 0: db-primary`)
     Actually, output each server on a new line: `Phase X: <hostname>`.
4. Compile your C program to `/home/user/resolver` and run it to generate `/home/user/backup_plan.log`.

Constraints:
- Do NOT use the `stale_routes_cache` table. 
- You must use C and the `libsqlite3` library to execute the database operations.
- The output file `/home/user/backup_plan.log` must contain exactly the calculated phases.

Ensure the final executable generates the file correctly.