You are a data engineer responsible for optimizing a real-time Graph ETL pipeline. 

The system relies on two services started via `/app/start_services.sh`:
1. **Data Source API**: A Flask application running on `http://127.0.0.1:8080`. It serves a bounded stream of user interaction events. Fetching from `http://127.0.0.1:8080/stream` returns a JSON array of 50,000 edge records: `{"src": "User123", "dst": "User456", "action": "follows"}`.
2. **Graph Database**: A Memgraph instance (Cypher-compatible) running locally on Bolt port `7687` (unauthenticated).

Currently, there is a badly written ETL script at `/home/user/etl_pipeline.py` that connects to the API, parses the JSON, and inserts the data into Memgraph one record at a time using `MERGE` without any indices. This takes roughly 45 seconds to complete.

Your objective is to:
1. **Optimize the Schema**: Create the appropriate index strategy in the graph database to accelerate node lookups.
2. **Rewrite the ETL Script**: Modify `/home/user/etl_pipeline.py` to use Cypher's `UNWIND` parameterization for bulk inserts (batching all 50,000 records in a single or a few queries) rather than looping inserts.
3. **Graph Analytics**: After the data is loaded, append logic to the Python script to execute a Cypher query that calculates the **PageRank** of all nodes (or use degree centrality if you prefer, but you must find the node with the highest out-degree). 
Wait, specifically, write a Cypher query to find the top 5 users by out-degree (number of "follows" relationships going out from them).
4. **Log the Output**: Write the JSON output of these top 5 users to `/home/user/top_users.json` in the exact format: `[{"user": "UserX", "out_degree": 150}, ...]`.

Requirements:
- You must use Python. The Neo4j Python driver (`neo4j`) is installed.
- The entire execution of `python3 /home/user/etl_pipeline.py` must complete in **under 3.0 seconds**.
- Do not modify the API or the Memgraph server configuration.

Please fix the script, ensure the services are communicating correctly, and write the final output.