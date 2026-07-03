You are assisting a financial compliance officer who is auditing an internal transaction system for potential money laundering networks. The auditing tool is written in C++ and interacts with a local SQLite database (`/home/user/compliance.db`). The tool currently suffers from multiple issues, including a query deadlock, poor performance on analytical queries, and missing capabilities for tracing financial networks.

You need to resolve these issues by completing the following three objectives:

**Objective 1: Resolve the Deadlock**
The existing C++ tool at `/home/user/audit_tool/main.cpp` spawns two concurrent threads to simulate concurrent auditing updates. Thread A updates the risk score of Account X then Account Y. Thread B simultaneously updates Account Y then Account X. Because of the reversed order, this consistently results in a deadlock (or an `SQLITE_BUSY` timeout in SQLite terms when using explicit transactions).
1. Modify `/home/user/audit_tool/main.cpp` to eliminate the deadlock by ensuring a consistent lock/update order (e.g., always update the account with the smaller ID first).
2. Ensure the code compiles. You can build it using `g++ -std=c++17 -pthread main.cpp -lsqlite3 -o audit_tool`.
3. Run `./audit_tool`. Upon success without deadlocking, it will write a file `/home/user/audit_tool/audit_success.log` containing the string "AUDIT_COMPLETE".

**Objective 2: Index Strategy for Window Functions**
The compliance team runs a heavy analytical query to calculate rolling 7-day transaction volumes per account. The query currently causes full table scans.
Write an SQL script at `/home/user/optimize.sql` containing the `CREATE INDEX` statements needed to optimize the following query. An optimal index must allow the query plan to avoid sorting and full table scans on the `transactions` table.
```sql
SELECT account_id, timestamp, amount,
       SUM(amount) OVER (
           PARTITION BY account_id 
           ORDER BY timestamp 
           ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
       ) as rolling_7_tx_sum
FROM transactions;
```

**Objective 3: Graph Traversal Query**
We suspect a cyclic laundering ring. The `transactions` table acts as a directed graph where `sender_id` is the source node and `receiver_id` is the target node. 
Write a SQLite query in `/home/user/path.sql` that uses a recursive Common Table Expression (CTE) to find the shortest transaction path from Account `101` to Account `205`. 
The query should output a single row containing `path_length` (the number of edges/transactions in the shortest path). 
Run your query and output the result to `/home/user/shortest_path.csv` (without headers) using the sqlite3 CLI.

**System Details:**
* The database schema is:
  `CREATE TABLE accounts (id INTEGER PRIMARY KEY, risk_score INTEGER);`
  `CREATE TABLE transactions (id INTEGER PRIMARY KEY, account_id INTEGER, sender_id INTEGER, receiver_id INTEGER, amount REAL, timestamp INTEGER);`
* Ensure all your scripts and logs are placed exactly at the specified paths.