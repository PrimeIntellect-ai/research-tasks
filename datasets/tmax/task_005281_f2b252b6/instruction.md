You are a data engineer tasked with optimizing a slow ETL pipeline and performing graph analytics. 

Your environment has three running services:
1. **PostgreSQL** (`localhost:5432`, DB: `company`, User: `postgres`, Password: `secret`): Contains relational user metadata in the `users` table (columns: `user_id`, `name`, `department`).
2. **MongoDB** (`localhost:27017`, DB: `logs`, Collection: `interactions`): Contains document-based interaction logs (fields: `source_id`, `target_id`, `interaction_type`, `timestamp`).
3. **Neo4j** (`localhost:7687`, User: `neo4j`, Password: `password123`): The target graph database.

Currently, there is a working but extremely inefficient Python ETL script located at `/app/naive_etl.py`. This script reads users from Postgres, reads interactions from MongoDB, and inserts them into Neo4j row-by-row using standard Cypher `CREATE` and `MERGE` statements. It maps relational rows to `User` nodes and document logs to `INTERACTED_WITH` relationships.

Your objectives:
1. **Optimize the ETL Pipeline:** Create a highly optimized Python script at `/home/user/fast_etl.py`. It must perform the exact same cross-representation mapping and data loading as `/app/naive_etl.py`, but it must be significantly faster. You should use batching techniques (e.g., Cypher's `UNWIND` clause) to minimize round-trips to the database. The automated verifier will measure the speedup: `(Time of naive_etl) / (Time of fast_etl)`. Your script must achieve a speedup of **at least 15.0x**.
2. **Graph Analytics:** Once the data is quickly loaded into Neo4j, write a second script `/home/user/analytics.py` that executes a Cypher query to calculate the out-degree centrality (number of outgoing `INTERACTED_WITH` relationships) for all users in the graph. The script must output the results to `/home/user/centrality.csv` with headers `user_id,out_degree`, sorted by `out_degree` descending, then by `user_id` ascending.

Note: Before running your new ETL, make sure to wipe the Neo4j database (`MATCH (n) DETACH DELETE n`) so you don't duplicate data.