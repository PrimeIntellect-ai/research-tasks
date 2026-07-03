You are a Database Reliability Engineer (DBRE) tasked with building a tool to calculate backup restoration costs. Your backup metadata is stored across two systems: a graph database tracking dependencies (incremental backups depending on previous backups) and a relational SQLite database tracking the size and timestamps of each backup.

Your goal is to build a C-based pipeline that processes a backup chain and calculates the cumulative restore size using analytical window functions.

Step 1: Graph Query (Cypher)
Write a Cypher query and save it to `/home/user/chain.cypher`. The query should find the path from a specific incremental backup (where `id = 'bkp_105'`) traversing the `DEPENDS_ON` relationship in the outgoing direction until it reaches a full backup (where `type = 'FULL'`). Return only the `id` property of all backups in this path. (You do not need to execute this query, just write the correct syntax).

Step 2: C Pipeline & Window Functions
A script will simulate the graph database output by providing a list of backup IDs to your C program via standard input (one ID per line).
Write a C program at `/home/user/pipeline.c` that:
1. Reads the list of backup IDs from standard input.
2. Connects to the SQLite database located at `/home/user/backups.db`.
3. Constructs and executes a SQL query that uses a **Window Function** to calculate the running total (cumulative sum) of the `size_mb` column for these specific backup IDs, ordered by `timestamp` ascending.
4. Extracts the final cumulative total (the sum of all sizes in the chain) and writes this single integer value to `/home/user/restore_cost.txt`.

Database Schema (`/home/user/backups.db`):
Table: `backup_metadata`
Columns: `id` (TEXT), `type` (TEXT), `size_mb` (INTEGER), `timestamp` (INTEGER)

Requirements:
- Your C program must use the SQLite3 C API (`sqlite3.h`).
- Your C program must compile successfully to `/home/user/pipeline` using `gcc /home/user/pipeline.c -o /home/user/pipeline -lsqlite3`.
- The output file `/home/user/restore_cost.txt` must contain exactly one integer and a newline.