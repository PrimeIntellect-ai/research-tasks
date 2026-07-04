You are a Database Reliability Engineer managing logical backups for a complex relational database schema. To maintain referential integrity during the backup process, tables must be backed up in the correct dependency order. 

You have been provided an SQLite database containing the schema relationships at `/home/user/metadata.db`.

It contains two tables:
1. `tables`: Columns are `id` (INTEGER PRIMARY KEY) and `name` (TEXT).
2. `deps`: Columns are `table_id` (INTEGER) and `depends_on_id` (INTEGER). This indicates that the table with `table_id` has a foreign key pointing to `depends_on_id`, meaning `depends_on_id` must be backed up first.

Your task is to:
1. Write a C program at `/home/user/planner.c` that connects to this database using the SQLite3 C API (`sqlite3.h`). 
2. Use a Recursive CTE (Graph Traversal) in a single SQL query to compute the backup order. You must calculate:
   - `table_name`: The name of the table.
   - `backup_level`: `0` if the table has no dependencies. Otherwise, it is `MAX(dependency backup_level) + 1`.
   - `path`: The shortest dependency chain from the current table down to a level 0 table, formatted as `current_table->dep1->dep2`. For level 0 tables, the path is just the table name itself. If there are multiple shortest paths, any valid shortest path is acceptable.
3. The C program must execute this query and output the results to a CSV file at `/home/user/backup_plan.csv`.
4. The CSV must have the exact header: `table_name,backup_level,path`.
5. The CSV rows must be sorted by `backup_level` ASC, then by `table_name` ASC.
6. Compile your program to `/home/user/planner` and run it to generate the CSV. You can assume `libsqlite3-dev` is installed, so you can compile with `gcc -o /home/user/planner /home/user/planner.c -lsqlite3`.

Ensure that the output CSV format strictly matches standard CSV formatting without trailing spaces.