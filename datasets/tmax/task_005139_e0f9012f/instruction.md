You are a Database Reliability Engineer. We have an SQLite database containing metadata about our backup infrastructure. Our backups are incremental, meaning each backup (except full backups) depends on a parent backup.

The database is located at `/home/user/backups.db` and has the following table:
`CREATE TABLE backups (id INTEGER PRIMARY KEY, parent_id INTEGER, size_mb INTEGER);`

You need to write a C program that analyzes this backup dependency graph using the SQLite C API (`sqlite3.h`). 

Your C program must be saved as `/home/user/analyzer.c` and compiled to an executable at `/home/user/analyzer` (link with `-lsqlite3`).

When executed, your program must perform the following analyses and generate two output files:

1. **Leaf Chain Analysis** (`/home/user/leaf_chains.csv`):
   Find all "leaf" backups (backups that are not a `parent_id` to any other backup). For each leaf backup, calculate the total size of its restoration chain. A restoration chain includes the leaf backup itself and all of its ancestors up to the root (where `parent_id` is NULL).
   The output CSV must contain the leaf backup IDs and their total restoration chain size (in MB), ordered by the total chain size in descending order.
   Format: `leaf_id,total_chain_size`

2. **Top Ancestor Analysis** (`/home/user/top_ancestor.txt`):
   Identify the single backup `id` that has the highest number of descendants in the dependency graph (a descendant is any backup that eventually traces its `parent_id` lineage back to this backup). If there is a tie, output the smallest `id`.
   The file should contain only this integer ID.

You should use SQLite's Recursive CTEs to traverse the graph and perform these aggregations efficiently inside the database query before writing the results to the files in C.