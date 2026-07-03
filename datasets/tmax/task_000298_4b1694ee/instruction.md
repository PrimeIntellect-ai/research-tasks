You are a Database Reliability Engineer. We have a backup pipeline that extracts knowledge graph data from a local PostgreSQL database and processes it through Redis before writing to an archive. Recently, the Python backup script has been causing deadlocks in Postgres due to concurrent transactions fighting over table locks during complex graph pattern matching queries.

We have set up a multi-service environment for you:
- PostgreSQL is running on localhost:5432 (database: `graphdb`, user: `postgres`, password: `postgres`).
- Redis is running on localhost:6379.

Your task is to write a Python CLI program at `/home/user/backup_extractor.py` that performs the backup extraction without deadlocking.

The CLI must accept two arguments:
1. `--start-node`: An integer ID representing the root node of the knowledge graph.
2. `--max-depth`: An integer specifying how many hops to traverse.

The script must:
1. Connect to Postgres and perform a graph traversal starting from `--start-node` up to `--max-depth`. The schema is a simple adjacency list in the `edges` table (`source_id` INT, `target_id` INT, `weight` FLOAT) and `nodes` table (`id` INT, `type` VARCHAR, `data` JSONB).
2. Filter out any nodes where `type` is 'transient'.
3. Sort the resulting nodes by their shortest path distance from the start node, then by `id` ascending.
4. Implement a pagination strategy (fetch size of 100) in your query pipeline to avoid locking the entire `edges` table. Read uncommitted or snapshot isolation is acceptable to prevent deadlocks with concurrent writers.
5. Chain the results into Redis, storing a JSON list of node IDs under the key `backup:path:<start-node>`.
6. Print the JSON list of extracted node IDs to stdout.

To verify your solution, our test harness will run your script against a reference oracle with various `--start-node` and `--max-depth` parameters. Your script's stdout must be bit-exact equivalent to the oracle's output.

Please ensure all dependencies (like `psycopg2` and `redis`) are installed and your script is executable.