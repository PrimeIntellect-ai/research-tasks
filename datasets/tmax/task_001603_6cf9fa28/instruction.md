You are tasked with stepping in as a database administrator to fix a querying issue in our graph processing pipeline. We have a multi-service setup containing a Redis instance (port 6379) and a backend application. The primary data store is an SQLite database located at `/app/data/graph.db`.

The database contains two tables representing a graph of users:
1. `nodes(id INTEGER PRIMARY KEY, name TEXT, score REAL, active INTEGER)`
2. `edges(src INTEGER, dst INTEGER)`

An index named `idx_edges_src` exists on `edges(src)`. Recently, a storage failure corrupted this index, causing it to return stale, ghost rows that have actually been deleted from the `edges` table. Because we cannot take the database offline to rebuild the index right now, we need a query workaround.

You must create a Python script `/home/user/solve.py` that takes exactly three integer command-line arguments: `<node_id> <limit> <offset>`. 

Your script must:
1. First, check the local Redis cache (running on localhost:6379, db=0) for the exact string key `graph:{node_id}:{limit}:{offset}`. If the key exists, print its value (which will be a JSON string) to standard output and exit.
2. If the key does not exist, query the SQLite database for all active neighbors of `<node_id>`. A neighbor is a node where `edges.src == <node_id>`, `edges.dst == nodes.id`, and `nodes.active == 1`.
3. Modify your SQL query to explicitly **bypass the corrupted index** `idx_edges_src`. You must force SQLite to scan the main `edges` table instead of the index (e.g., by using query plan manipulation techniques like the unary `+` operator or `NOT INDEXED`). Do not alter the database schema or drop the index.
4. The results must be sorted by `nodes.score` in DESCENDING order. If there is a tie, sort by `nodes.id` in ASCENDING order.
5. Apply the requested `<limit>` and `<offset>` for pagination.
6. Format the results as a JSON array of objects, e.g., `[{"id": 5, "name": "Alice", "score": 9.5}, ...]`.
7. Store this exact JSON string in Redis under the key `graph:{node_id}:{limit}:{offset}`.
8. Print the JSON string to standard output.

Do not print anything else to standard output besides the JSON array. Your script must be self-contained and run using standard Python 3. You may use the `redis` and `sqlite3` packages.