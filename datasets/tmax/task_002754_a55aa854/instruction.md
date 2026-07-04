You are a data engineer tasked with optimizing an ETL pipeline that maps relational network topology data into a graph database to perform shortest-path computations.

Environment:
A multi-service architecture is deployed in your environment, managed by a startup script at `/app/start_services.sh`. The services include:
1. **PostgreSQL**: Stores the relational source data (routers and links).
2. **Neo4j**: The target graph database.

Currently, the services are not communicating properly due to a misconfiguration in the environment variables located at `/home/user/config.env`. 

Your tasks:
1. **Service Reconfiguration**: Fix `/home/user/config.env` so that the Bash ETL script can authenticate and connect to both PostgreSQL (port 5432) and Neo4j (port 7687). The PostgreSQL user is "admin" with password "adminpass", database "network_db". The Neo4j user is "neo4j" with password "graphpass".
2. **ETL Optimization**: There is a naive Bash ETL script at `/home/user/etl.sh` that extracts topology records from PostgreSQL and inserts them into Neo4j one by one using `cypher-shell`. It is prohibitively slow. Rewrite `/home/user/etl.sh` (in Bash) to perform a bulk data transfer. You should extract the relational data (tables: `routers` and `links`), map it into a compatible document/CSV format, and use Neo4j's bulk loading capabilities (e.g., `LOAD CSV` via `cypher-shell`) to create `(:Router)` nodes and `[:CONNECTED_TO {latency: ...}]` relationships.
3. **Graph Query Construction**: Once the data is successfully loaded, write a Cypher query in the file `/home/user/shortest_path.cypher` that finds the shortest path between the router with `name = 'SOURCE_ROUTER'` and `name = 'DEST_ROUTER'`, minimizing the sum of the `latency` property on the relationships. The query should return the total latency as an integer alias `total_latency`.

The verification suite will run your `/home/user/etl.sh` script and measure its execution time against a reference implementation. It will then execute your `/home/user/shortest_path.cypher` query to verify correctness. 
Ensure your ETL script handles cross-representation mapping efficiently and completely.