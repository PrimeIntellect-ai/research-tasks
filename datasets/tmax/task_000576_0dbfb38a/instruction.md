You are an AI assistant helping a data researcher optimize a fragile data pipeline.

We have a multi-service architecture running locally:
1. **PostgreSQL** (port 5432, db: `research`, user: `postgres`, password: `password`) containing academic metadata.
2. **Redis** (port 6379, no password) used as a graph projection store.
3. A background Python worker (`/app/traffic_generator.py`) that continuously updates author scores in the database to simulate real-time ingestion.

The researcher has an existing script `/app/extract_graph.py` which is supposed to:
1. Extract authors who have an average citation score above 50.0.
2. For those authors, find all other authors they have cited.
3. Aggregate this into a summarized graph.
4. Materialize the projection into Redis.

**The Problem:**
Currently, `/app/extract_graph.py` is extremely slow (taking over 30 seconds) and frequently crashes due to deadlocks. The original author used `SELECT ... FOR UPDATE` extensively, which collides with the background `traffic_generator.py` worker. Furthermore, it uses a naive N+1 query pattern.

**Your Task:**
Rewrite `/app/extract_graph.py` to be efficient and completely avoid deadlocks. 
1. Modify the PostgreSQL schema if necessary (e.g., adding indexes) using the `psql` CLI.
2. Rewrite the query logic in `/app/extract_graph.py` to use a single efficient CTE/window function instead of N+1 queries. Remove the unnecessary locking that causes deadlocks. 
3. The script must materialize the projected graph into Redis exactly as follows:
   - For every author extracted (score > 50.0):
     - Set a Redis string key: `author:{author_id}:score` with their score (rounded to 2 decimal places).
     - Set a Redis Set key: `author:{author_id}:cites` containing the IDs of all authors they cite.
4. The script must execute from start to finish in **under 2.5 seconds**.

You can run `python /app/extract_graph.py` to test your implementation. The automated verifier will measure the exact execution time of your script and check the correctness of the Redis keys. Ensure your solution is robust to the concurrent updates happening in the background.