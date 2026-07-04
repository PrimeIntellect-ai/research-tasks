You are acting as a Database Reliability Engineer (DBRE). We have a legacy distributed backup system consisting of three cooperating services running locally:
1. A PostgreSQL instance (port 5432) storing relational metadata about database schemas and their foreign-key dependencies.
2. A Redis instance (port 6379) acting as a document/key-value store that tracks physical backup chunks and their storage URLs.
3. A Python Flask metadata service (port 5000) that exposes an endpoint `/api/v1/topology/<db_id>` returning JSON documents about how backup chunks depend on each other (incremental backup chains).

Your task is to write a standalone Python CLI tool at `/home/user/workspace/restore_planner.py` that computes the optimal, ordered sequence of backup chunks to restore a specific database and all its dependencies.

To do this, your tool must:
1. Take a single argument: `--db-id <ID>`
2. Query PostgreSQL to find all upstream database dependencies (recursively mapping the relational graph).
3. Call the Flask API to get the incremental backup chain for each required database.
4. Use Redis to look up the final storage paths for all required chunk IDs.
5. Perform graph analytics (topological sort and out-degree centrality) to order the restore operations: databases with the highest number of incoming dependencies must be restored first. Within a single database, incremental chunks must be applied in exact chronological chain order.
6. Print the final execution pipeline to `stdout` strictly as a comma-separated list of storage URLs.

There is a reference oracle at `/app/oracle_planner` that performs this exact calculation. Your script must be bit-exact equivalent in its output to this oracle for any valid `--db-id`.

You will need to ensure the services are properly connected. The Flask service in `/app/flask_service` is currently misconfigured and trying to connect to a legacy Redis port (6380) and Postgres port (5433). You must fix its `config.env` file and restart the services using the provided `/app/start_services.sh` script before writing your tool.

Write `/home/user/workspace/restore_planner.py` using standard libraries and `psycopg2` / `redis` / `requests`.