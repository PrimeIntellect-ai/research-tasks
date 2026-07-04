You are a data engineer tasked with fixing and completing an ETL pipeline that computes graph analytics.

We have a multi-service setup located in `/app/`. The system consists of:
1. An SQLite database (`/app/data/graph.db`) containing two tables: `nodes(id)` and `edges(source, target)`.
2. A Redis server running locally on port 6379 used for caching graph metrics.
3. A bash-based TCP service (`/app/service/query_server.sh`) that listens on port 8080 and responds to node queries.

The pipeline is currently broken due to a few issues:
1. The SQLite database has a corrupted index on the `edges` table, which causes queries to return stale or duplicate rows. You need to analyze the schema, drop the bad index, and recreate a proper index on `(source, target)`.
2. You need to write a bash script `/app/etl/compute_metrics.sh` that uses `sqlite3` to compute the Out-Degree Centrality for each node. Use SQL window functions or aggregations to rank the nodes by their out-degree (highest degree gets rank 1). 
3. The script must load these computed metrics into Redis. For each node, set a Redis key `node:<id>:rank` with its computed rank.
4. Finally, you need to fix the `query_server.sh` script so that when it receives a node ID over TCP, it fetches the rank from Redis and outputs exactly `Rank: <rank>`.

Your tasks:
- Fix the corrupted index in `/app/data/graph.db`.
- Implement `/app/etl/compute_metrics.sh` (using `sqlite3`, `redis-cli`, and bash coreutils).
- Execute the ETL script to populate Redis.
- Fix `/app/service/query_server.sh` to correctly read from Redis and return the result. Ensure the server runs in the background listening on port 8080 using `nc` or `socat`.

Do not use Python or other high-level languages for the implementation; stick to bash, `sqlite3`, and `redis-cli`.