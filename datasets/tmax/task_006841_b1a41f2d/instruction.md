You are a Database Reliability Engineer investigating an issue with a backup verification tool.

We have a SQLite database at `/home/user/backup_meta.db` that stores the metadata of our backed-up files. Because file metadata can be highly variable, the specific file attributes are stored in a JSON string column called `metadata`.

The table schema is:
`files(id INTEGER PRIMARY KEY, parent_id INTEGER, name TEXT, metadata TEXT)`

There is a C program located at `/home/user/check_backup.c` which is intended to calculate the total size of all files contained within a specific directory (including all subdirectories) using a recursive Common Table Expression (CTE) and JSON aggregation.

However, the program currently has two major problems:
1. **Incorrect Results:** The recursive CTE is returning incorrect results. It appears there is a bug in the join condition of the recursive step (an implicit cross join or self-join error).
2. **Security & Performance:** The program constructs the SQL query using `sprintf` with string interpolation. This prevents the database from reusing query plans and opens it up to SQL injection.

Your task is to:
1. Fix the recursive CTE in `/home/user/check_backup.c` so it correctly traverses the parent-child hierarchy.
2. Refactor the C code to use SQLite parameterized queries (e.g., `?` placeholders and `sqlite3_bind_int` or similar) instead of `sprintf` for injecting the target directory ID.
3. Compile the fixed program into `/home/user/check_backup` (ensure you link the sqlite3 library: `gcc -o check_backup check_backup.c -lsqlite3`).
4. Run the compiled program for the directory with ID `1` and redirect its standard output to `/home/user/result.txt`.

The program should print a single integer representing the total size in bytes.

*Note: The `metadata` JSON object contains a `size` field (integer) and a `type` field (either `"file"` or `"dir"`). Only sum the sizes of entries where the type is `"file"`.*