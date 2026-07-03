You are a Database Reliability Engineer investigating backup chain integrity and storage usage. You have been given an undocumented SQLite database located at `/home/user/backups.db` which contains backup execution logs and NoSQL-style JSON metadata for a fleet of databases.

Your task is to write a C++ program `/home/user/analyze_backups.cpp` that connects to this SQLite database, processes the data, and writes a summary report to `/home/user/report.txt`.

You must perform the following:
1. **Data Model Reverse Engineering**: Inspect `/home/user/backups.db` to understand its schema. The main table contains backup events, parent-child relationships (for incremental backups), and a JSON column storing NoSQL-style metadata.
2. **Window Functions & Analytical Aggregation**: Write a SQL query in your C++ program that uses window functions (e.g., `ROW_NUMBER()` or `RANK()`) to identify the *most recent* 'full' backup (by timestamp) for each distinct `dataset`.
3. **NoSQL Aggregation**: Query the JSON metadata column using SQLite's JSON functions. Calculate the sum of the `size_bytes` field extracted from the JSON metadata for all backups where the JSON `status` field is exactly `"archived"`.
4. **Graph Projection and Materialization**: Extract the `id` and `parent_id` columns for all backups. Build a directed graph data structure in C++ representing the backup dependency chains (a parent is required to restore its child). Calculate the length of the longest restoration chain in the entire database (the maximum number of edges from a 'full' backup to its furthest 'incremental' descendant).

Your C++ program must output a report to `/home/user/report.txt` in exactly this format:
```
Total Archived Size: <total_bytes>
Max Restoration Chain Length: <integer>
Latest Full Backups:
<dataset_name_1>: <backup_id>
<dataset_name_2>: <backup_id>
... (alphabetical by dataset name)
```

Compile your code using `g++ -std=c++17 /home/user/analyze_backups.cpp -lsqlite3 -o /home/user/analyze_backups` and execute it to generate the report. Ensure all dynamically allocated memory in your C++ graph structure is properly freed.