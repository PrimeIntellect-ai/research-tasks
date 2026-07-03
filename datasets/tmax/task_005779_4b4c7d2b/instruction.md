You are a Database Reliability Engineer managing a sharded database architecture. We have several SQLite database backup files representing different shards of our system. Recently, we've noticed performance degradation across our shards and suspect missing indexes on foreign keys, as well as uneven data distribution.

Your task is to write a Go program that analyzes these database backups, aggregates data, and identifies missing indexing strategies.

**Environment details:**
- Go is installed on the system.
- The SQLite backups are located in `/home/user/backups/`. There are three shards: `shard_1.db`, `shard_2.db`, and `shard_3.db`.
- Each database contains two tables: `users` and `orders`. 
- You may use the `github.com/mattn/go-sqlite3` package. You will need to initialize a Go module in `/home/user/workspace` and fetch the dependency.

**Requirements for your Go program:**
1. **Schema Analysis & Relationship Mapping**: Connect to each SQLite database and read the schema for the `orders` table. Identify any columns that act as foreign keys (e.g., referencing the `users` table).
2. **Cross-query Aggregation**: Count the total number of rows in the `users` table and the `orders` table across *all* shards combined.
3. **Index Strategy Design**: Check the existing indexes in the databases. If a foreign key column in the `orders` table does not have an index, generate the appropriate `CREATE INDEX` statement to optimize join queries.

Your Go program must create a JSON report at `/home/user/report.json` with the exact following structure:
```json
{
  "total_users": 0,
  "total_orders": 0,
  "missing_indexes": [
    "CREATE INDEX idx_orders_user_id ON orders(user_id);"
  ]
}
```
*(Note: Replace the integer values with the actual aggregated counts, and ensure the missing index statement follows the exact format: `CREATE INDEX idx_<table_name>_<column_name> ON <table_name>(<column_name>);`)*

Write, compile, and execute the Go program to generate the required report.