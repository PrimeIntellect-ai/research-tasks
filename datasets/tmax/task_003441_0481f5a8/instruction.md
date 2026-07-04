You are a Database Reliability Engineer. Recently, concurrent backup jobs for our internal infrastructure knowledge graph have been deadlocking and failing due to poor transaction management. Your task is to write a clean, efficient Python script that performs a graph projection, materializes the result safely, and exports it for the backup archive.

We store our infrastructure knowledge graph in an SQLite database located at `/home/user/graph.db`.
The database has two tables:
- `Nodes` (`id` INTEGER PRIMARY KEY, `label` TEXT, `name` TEXT)
- `Edges` (`src` INTEGER, `dst` INTEGER, `rel` TEXT)

Your goal is to write and execute a Python script at `/home/user/graph_export.py` that does the following:
1. **Graph Pattern Matching**: Query the graph to find all implicit access paths where a `User` manages a service that depends on a database. Specifically, find all paths matching this pattern:
   `(Node with label 'User') -[rel 'MANAGES']-> (Node with label 'Service') -[rel 'DEPENDS_ON']-> (Node with label 'Database')`
2. **Graph Materialization**: Create a new table named `user_db_access` in the same database with two columns: `user_name` (TEXT) and `db_name` (TEXT). Insert the names of the matched Users and Databases into this table. Ensure you use a single, clean transaction for the insertion to avoid the deadlocks we've been seeing. Clear the table first if it already exists.
3. **Query Result Export**: Query the `user_db_access` table, sort the results alphabetically by `user_name` ascending, and then by `db_name` ascending. Export these sorted results to a JSON file at `/home/user/backup_view.json`.

The exported JSON must be a list of objects exactly matching this format:
```json
[
  {
    "user": "Alice",
    "database": "UsersDB"
  },
  ...
]
```

Write the Python script, execute it to ensure the table and JSON file are created correctly, and ensure your script handles the database connection and transactions cleanly.