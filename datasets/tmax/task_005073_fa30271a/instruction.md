You are a data analyst tasked with processing a large network dataset using PostgreSQL, Redis, and Python. We have a multi-service environment where a startup script (`/app/start_services.sh`) initializes a PostgreSQL database (port 5432) and a Redis instance (port 6379). 

Your goal is to build an end-to-end pipeline that loads data, filters it using advanced SQL, computes graph analytics, and caches the results.

Here is the step-by-step requirement:
1. **Service Configuration**: The services are started by `/app/start_services.sh`. Ensure you can connect to PostgreSQL (user: `postgres`, password: `postgres`, db: `postgres`) and Redis (localhost:6379, no password). Create a new database named `graph_analytics`.
2. **Data Ingestion**: You are provided with a CSV file at `/home/user/data/interactions.csv` with columns: `source_id`, `target_id`, `timestamp`, `interaction_weight`. Load this data into a PostgreSQL table named `raw_interactions` in the `graph_analytics` database.
3. **Analytical Filtering (SQL)**: Write a Python script `/home/user/process_graph.py` that connects to PostgreSQL and uses a SQL Window Function to extract a filtered dataset. For each `source_id`, extract only their top 3 interactions based on `interaction_weight` (descending). If there is a tie, order by `timestamp` (ascending), then `target_id` (ascending). 
4. **Graph Processing**: Using the filtered records, construct a directed graph in Python using the `networkx` library. The edges should have the `interaction_weight` as an edge attribute. Calculate the PageRank of all nodes in this filtered graph using `networkx.pagerank` with `alpha=0.85` and `weight='interaction_weight'`.
5. **Cross-Service Export**: 
    - Store the calculated PageRank scores in Redis as a Hash named `node_pageranks`, where the key is the node ID (as a string) and the value is the PageRank score (as a string).
    - Export the top 20 nodes with the highest PageRank scores to a CSV file at `/home/user/top_nodes.csv` with columns `node_id` and `pagerank_score`, ordered by score descending (and node_id ascending for ties).

Your final deliverable is the executed `/home/user/process_graph.py` script that leaves the database populated, the Redis hash created, and the CSV file correctly formatted. Ensure all dependencies (like `psycopg2-binary`, `networkx`, `pandas`, `redis`) are installed in your environment.