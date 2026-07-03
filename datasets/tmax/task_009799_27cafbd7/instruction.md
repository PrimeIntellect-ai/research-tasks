You are a Database Reliability Engineer (DBRE) investigating a persistent database freeze. The system's transaction audit logs have been dumped into a local SQLite database, and you suspect that concurrent transactions have deadlocked, creating an infinite wait cycle.

Your goal is to build a C++ tool that analyzes the lock requests, maps the relational data into a Wait-For Graph, detects the deadlocked transactions, and optimizes the database schema for future analyses.

Here are your instructions:

1. **Environment Setup:** 
   The database dump should be located at `/home/user/audit.db`. Since it might not exist yet, assume the system has just exported it. The table schema is:
   `locks (tx_id INTEGER, resource TEXT, mode TEXT, status TEXT)`
   *Status can be 'GRANTED' or 'WAITING'.*

2. **Graph Mapping & Deadlock Detection (C++):**
   Write a C++ program at `/home/user/detect_deadlocks.cpp`. 
   The program must connect to `/home/user/audit.db` using the SQLite C/C++ API (`sqlite3.h`).
   It must query the `locks` table to build a Wait-For Graph. A directed edge exists from Transaction A to Transaction B if Transaction A is 'WAITING' for a resource that Transaction B currently holds ('GRANTED').
   The program must traverse this graph to find deadlocks (cycles).

3. **Output Generation:**
   Once the deadlock cycle is found, your C++ program must write the IDs of the deadlocked transactions to `/home/user/deadlock_report.txt`. 
   Format: A single line containing the deadlocked `tx_id`s, separated by commas, sorted in ascending numerical order (e.g., `42,55,102`).

4. **Query Optimization:**
   To ensure future runs of this script (or similar recursive CTEs) are performant, execute a SQL command against `/home/user/audit.db` to create a covering index named `idx_locks` on the `locks` table that optimizes the lookup of who holds the lock a waiting transaction needs.

Compile your program using `g++ -std=c++17 /home/user/detect_deadlocks.cpp -lsqlite3 -o /home/user/detect_deadlocks` and run it to produce the report. You may install any necessary development packages (like `libsqlite3-dev`) using the package manager.