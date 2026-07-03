You are a Database Reliability Engineer responsible for managing complex database restoration plans. Our systems consist of multiple microservice databases that have strict restoration dependencies (e.g., an `orders` database cannot be restored until the `users` database it depends on is fully restored).

We have a SQLite database at `/home/user/db_metadata.sqlite` that tracks our databases, their dependency graphs, and all backup metadata.

The database has the following schema:
```sql
CREATE TABLE databases (
    id INTEGER PRIMARY KEY, 
    name TEXT UNIQUE
);

CREATE TABLE dependencies (
    parent_id INTEGER, 
    child_id INTEGER,
    FOREIGN KEY(parent_id) REFERENCES databases(id),
    FOREIGN KEY(child_id) REFERENCES databases(id)
);
-- "child_id" depends on "parent_id". 
-- This means the database represented by parent_id MUST be restored BEFORE child_id.

CREATE TABLE backups (
    id INTEGER PRIMARY KEY, 
    db_id INTEGER, 
    size_bytes INTEGER, 
    backup_timestamp DATETIME, 
    status TEXT, -- 'SUCCESS' or 'FAILED'
    FOREIGN KEY(db_id) REFERENCES databases(id)
);
```

Your task is to write a robust Bash script located at `/home/user/analyze_backups.sh` that dynamically calculates the correct restoration order for a specific target database and aggregates the latest valid backups.

The script must accept exactly two arguments:
1. The target database name (e.g., `analytics`)
2. A cutoff timestamp in `YYYY-MM-DD HH:MM:SS` format

The script should perform the following logic (using `sqlite3` and Bash):
1. Find all databases that must be restored to support the target database. This includes the target database itself, its direct dependencies, its dependencies' dependencies, and so on (recursive hierarchical querying).
2. Determine the correct restoration order. Databases must be ordered by their maximum dependency depth from the target database in descending order (i.e., the most fundamental databases are restored first). If two databases have the same maximum depth, order them alphabetically by database name ascending. The target database will have depth 0.
3. For each database in the restoration order, find the single most recent backup where `status = 'SUCCESS'` and the `backup_timestamp` is strictly less than the cutoff timestamp provided as the second argument.
4. Calculate the sum of `size_bytes` for all selected backups.
5. Output the final plan to a file named `/home/user/restore_plan.txt`.

The format of `/home/user/restore_plan.txt` must exactly match the following:
```
Total Size: <sum_of_size_bytes>
Restoration Order:
1. <db_name> - <backup_id> - <backup_timestamp>
2. <db_name> - <backup_id> - <backup_timestamp>
...
```
(Note: The list numbering must start at 1 and follow the calculated restoration order).

Ensure the script is executable and handles the logic entirely locally. Do not hardcode the expected outputs for specific test cases, as the test suite will run your script with different arguments and check the resulting `restore_plan.txt`.

To verify your work, run your script with:
`./analyze_backups.sh analytics "2023-10-01 00:00:00"`