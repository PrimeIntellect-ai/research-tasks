You are an analyst at a database monitoring company. We have a pipeline that captures concurrent transaction waits and exports them as CSVs. You need to implement a Rust-based worker that detects deadlocks (cycles in the wait-for graph) and identifies the root cause using graph centrality, integrating with our local database and caching layer.

Your task has three parts:

1. **Environment Setup (Multi-Service)**
   In `/home/user/services`, there is a `docker-compose.yml` defining two services:
   - `postgres_db` (PostgreSQL)
   - `redis_cache` (Redis)
   Start these services. The PostgreSQL database `monitoring` (user: `admin`, pass: `secret`) contains a table `deadlock_reports (file_name TEXT, is_deadlocked BOOLEAN, root_cause_tx INT, root_query TEXT)`. Redis contains query metadata hashes. 

2. **Rust Application Implementation**
   In `/home/user/app/deadlock_detector`, initialize a Rust binary project. The compiled binary (`target/debug/deadlock_detector`) must accept a single CLI argument: the path to a CSV file.
   
   The CSV files have the following headers: `tx_id,waiting_for_tx_id,query_hash`
   - Build a directed graph where an edge goes from `waiting_for_tx_id` to `tx_id` (since `tx_id` is blocked by `waiting_for_tx_id`).
   - Determine if there is a cycle (deadlock).
   - If there is a cycle, find the "root cause" transaction within the cycle, defined as the node involved in the cycle with the highest in-degree centrality (most other transactions waiting on it, directly or indirectly). Break ties by the lowest `tx_id`.
   - Fetch the actual SQL query for the root cause transaction from Redis using `HGET queries <query_hash>`.
   - Insert a row into the PostgreSQL `deadlock_reports` table.
   - **Crucial Exit Codes**: 
     - If the CSV contains a deadlock (cycle), the program MUST exit with code `1`.
     - If the CSV is a valid DAG (no deadlock), the program MUST exit with code `0`.

3. **Validation**
   Your binary will be tested against an adversarial corpus of CSVs. 
   - `/home/user/corpora/clean/` contains 50 CSVs with complex dependency DAGs but no cycles.
   - `/home/user/corpora/evil/` contains 50 CSVs with obfuscated cycles (deadlocks).
   Your tool must perfectly distinguish between them based on its exit codes.