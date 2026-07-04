You are a Database Reliability Engineer (DBRE) tasked with optimizing the backup schedule for a massive microservices architecture. The system contains thousands of databases with strict backup dependencies (e.g., the Identity database must be backed up before the Billing database to ensure foreign key consistency in the analytical warehouse).

The entire backup dependency graph is stored in an SQLite database located at `/home/user/backup_deps.db`. 

The database contains two tables:
1. `databases`:
   - `id` (INTEGER PRIMARY KEY)
   - `name` (TEXT)
   - `backup_time` (INTEGER): The time in minutes it takes to back up this specific database.
2. `dependencies`:
   - `source_id` (INTEGER): The ID of the database that MUST be backed up first.
   - `target_id` (INTEGER): The ID of the database that depends on the source.

All backups can run in parallel, provided their dependencies have finished backing up. 

Your task is to analyze the schema, extract the relationships, and compute the **critical path** of the backup process. The critical path is the sequence of dependent databases that dictates the absolute minimum time required to complete all backups (i.e., the path through the Directed Acyclic Graph with the highest total `backup_time`).

Perform the following steps:
1. Write a script in your language of choice to query `/home/user/backup_deps.db`. If you need indexes to speed up your queries, you should create them.
2. Calculate the total time (in minutes) of the critical path. Write this single integer value to `/home/user/critical_path_time.txt`.
3. Identify the sequence of database names that make up this critical path, from the initial source to the final target. Write this comma-separated list of database names to `/home/user/critical_path_sequence.txt` (e.g., `db_14,db_902,db_44`). If there are multiple paths with the exact same maximum time, pick the one where the string representation of the names sorted lexicographically is smallest, but for this dataset there is a strictly unique critical path.
4. Save the SQLite query execution plan (EXPLAIN QUERY PLAN) you used to extract the joined dependency data to `/home/user/query_plan.txt`.

Ensure your scripts handle large datasets efficiently.