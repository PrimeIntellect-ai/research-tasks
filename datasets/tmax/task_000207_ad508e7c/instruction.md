You are a Database Reliability Engineer tasked with managing a database that tracks file backup chains. You need to identify and process "orphaned" incremental backups to calculate how much storage space can be reclaimed.

You have a SQLite database located at `/home/user/backups.db`. It contains a single table:
`backups(id INTEGER PRIMARY KEY, parent_id INTEGER, size_bytes INTEGER, status TEXT)`

A backup chain starts with a full backup (where `parent_id IS NULL`) and is followed by incremental backups (where `parent_id` points to the previous backup in the chain). 
A backup is considered "orphaned" if:
1. Its `status` is `'active'`.
2. It is disconnected from any valid root backup. A valid root backup is one where `parent_id IS NULL` AND `status = 'active'`. If a backup traces its ancestry back to a deleted root, a missing root, or has an infinite loop without a valid active root, it is orphaned.

Your task:
1. Write a C++ program at `/home/user/process_backups.cpp` that connects to the SQLite database.
2. In your C++ program, first execute a SQL statement to design and create a query optimization index named `idx_parent_id` on the `parent_id` column to speed up hierarchical traversals.
3. Using a recursive query (CTE), calculate the cross-query aggregation: the sum of `size_bytes` for all orphaned active backups. 
4. The C++ program should write this single integer sum to a file named `/home/user/orphaned_size.txt`.

Ensure your C++ program compiles successfully (you may need to install `libsqlite3-dev` and link `-lsqlite3` during compilation) and runs to produce the correct output file. Only the final output file `/home/user/orphaned_size.txt` will be evaluated.