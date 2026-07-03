You are helping a researcher organize and query a complex graph of dataset dependencies. 

We have a local environment with a PostgreSQL database and a Redis cache that stores dataset metadata and their dependency graph. However, the system is currently broken in two ways:
1. The services are not properly glued together. The configuration file is misconfigured.
2. The primary querying script (`/home/user/dataset_query.py`) contains a critical SQL bug. It attempts to find all downstream datasets up to a certain depth, but due to a poorly written query with an implicit cross join, it returns massive amounts of incorrect, duplicated data.

Your tasks:
1. **Service Configuration:** 
   Start the services using `/app/start_services.sh`. Ensure the environment variables in `/home/user/config.env` are correctly set so that the Python script can communicate with PostgreSQL (running on port 5432, db name: `research_db`, user: `researcher`, password: `password123`) and Redis (running on port 6379).

2. **Fix the Query Script:**
   The script `/home/user/dataset_query.py` accepts four arguments: `--dataset-id`, `--max-depth`, `--limit`, and `--offset`. 
   Reverse engineer the schema from the database and rewrite the SQL query in `/home/user/dataset_query.py`. 
   The query must:
   - Perform a graph traversal to find all downstream dependencies (targets) starting from the given `--dataset-id`, up to `--max-depth` levels deep.
   - Include the starting dataset itself (depth 0).
   - Only include datasets where `is_active = true`.
   - Return a strictly JSON-formatted list of unique dataset IDs, sorted in ascending order.
   - Apply the given `--limit` and `--offset` for pagination on the final sorted list of IDs.

To ensure your fix is perfectly correct, your updated script must produce bit-exact identical JSON output to a reference oracle binary located at `/app/oracle_query` for any combination of valid inputs.

You can test the oracle to understand the expected output format:
`/app/oracle_query --dataset-id 5 --max-depth 2 --limit 10 --offset 0`

Please fix the configuration and the Python script so that it behaves exactly like the oracle.