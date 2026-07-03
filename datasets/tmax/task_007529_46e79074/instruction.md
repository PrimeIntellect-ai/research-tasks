You are acting as a Database Administrator and C++ Developer. We have an SQLite database located at `/home/user/topology.db` that represents a service dependency knowledge graph. Recently, an incomplete migration caused the database to perform poorly, and it contains some stale data that needs to be filtered out.

Your task has three phases:

1. **Database Optimization**:
   The `edges` table has an index named `idx_source` that is inefficient. You must connect to the SQLite database (using the `sqlite3` CLI) and execute commands to `REINDEX` the database and `VACUUM` it to ensure optimal performance.

2. **C++ Query Tool Implementation**:
   Write a C++ program at `/home/user/analyzer.cpp` that queries this SQLite database. Your program must use the SQLite C/C++ API (`<sqlite3.h>`). 
   
   The database schema is:
   - `services (id INTEGER PRIMARY KEY, name TEXT, is_active INTEGER)`
   - `dependencies (source_id INTEGER, target_id INTEGER, latency_ms INTEGER)`
   
   Your C++ program should execute a **Recursive CTE** (Common Table Expression) to find the "critical path" (the path with the highest total latency) from the service named 'API_GATEWAY' to the service named 'DATABASE_PRIMARY'. 
   - You must ONLY consider services where `is_active = 1`.
   - You must calculate the sum of `latency_ms` along the paths.

3. **Execution and Logging**:
   Compile your C++ program using `g++`:
   `g++ -std=c++17 /home/user/analyzer.cpp -lsqlite3 -o /home/user/analyzer`
   
   Run the program. It must output a single line to `/home/user/critical_path.txt` in the following format:
   `MAX_LATENCY: <integer_value>`

Ensure your C++ code checks for SQLite execution errors and handles them gracefully. Do not use external libraries other than the standard library and `sqlite3`.