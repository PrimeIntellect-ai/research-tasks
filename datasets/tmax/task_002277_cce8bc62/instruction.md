You are a data engineer tasked with fixing and optimizing a poorly performing graph ETL pipeline. 

The system consists of three services running locally:
1. A Redis cache.
2. A mock Data API (`sqlite_server.py` on port 5001) that serves graph data from an SQLite database (`/app/graph.db`).
3. An ETL API (`etl_api.py` on port 5000) that is supposed to fetch edges from the Data API, compute graph analytics, cache the results, and serve them.

Currently, the pipeline is extremely slow and incomplete. 

Your tasks:
1. **Reverse Engineer & Optimize the DB**: Inspect the SQLite database at `/app/graph.db`. The Data API queries edges filtered by a minimum weight, but this query is agonizingly slow because the schema lacks proper indexing. Identify the query pattern and create the optimal covering index directly in `/app/graph.db` to speed up the retrieval.
2. **Implement Graph Analytics**: Complete the `compute_and_cache_pagerank()` function in `/app/etl_api.py`. It must:
   - Fetch edges from `http://localhost:5001/edges?min_weight=0.85`
   - Build a directed graph.
   - Compute PageRank using NetworkX with default parameters.
   - Identify the top 10 node IDs with the highest PageRank scores.
   - Store this exact list of 10 integers as a JSON array in Redis under the key `top_pagerank` with a TTL of 60 seconds.
   - Return the JSON array.
3. **End-to-End Test**: Ensure that when `GET http://localhost:5000/pagerank` is called, it returns the correct JSON list of 10 integers in less than 0.5 seconds on average (after caching, and < 2 seconds for the initial computation).

The startup script `/app/start.sh` is used to launch all services. You can restart the services using this script while you develop.

Deliverables:
- The modified `/app/graph.db` with the new index.
- The fixed `/app/etl_api.py` running on port 5000.