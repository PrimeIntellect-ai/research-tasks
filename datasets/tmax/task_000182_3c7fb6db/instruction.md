You are a data engineer tasked with building an ETL pipeline that translates a relational event log into a graph database to perform fast analytical path queries.

We have a multi-service environment simulating our local staging infrastructure. A startup script at `/app/start_services.sh` spins up two background services:
1. **PostgreSQL** on `localhost:5432` (User: `postgres`, Password: `postgres`, DB: `analytics`)
2. **Memgraph** (a Cypher-compatible graph database) on `localhost:7687` (No auth required)

The Postgres database contains a table `raw_events` with the following schema:
- `event_id` (INTEGER)
- `user_id` (INTEGER)
- `event_timestamp` (TIMESTAMP)
- `event_type` (VARCHAR)

Your objectives:
1. **Cross-Representation Mapping (ETL):** Write a Python script at `/home/user/etl.py` that connects to both Postgres (using `psycopg2` or similar) and Memgraph (using `neo4j` Python driver). 
2. **Analytical SQL:** In your ETL, use SQL Window Functions to extract sequential events. An edge `(A)-[:NEXT]->(B)` exists if event `B` immediately follows event `A` for the *same* `user_id`, and `B` occurs within 60 minutes after `A`.
3. **Graph Materialization:** Insert these events as nodes `(:Event {event_id, event_type})` and relationships `(:Event)-[:NEXT]->(:Event)` into Memgraph.
4. **Index Strategy Design:** Create necessary indexes and/or constraints in Memgraph via Cypher so that querying event patterns is highly optimized.
5. **Graph Query:** Write a Cypher query and save it exactly at `/home/user/target_query.cypher`. The query must find the most frequent 3-step sequence of event types (e.g., 'login' -> 'view_item' -> 'purchase'). Return a single row with three columns `step1`, `step2`, `step3`, and an alias `frequency` representing the count.

**Performance Verification:**
Your graph database structure and query must be highly optimized. Once your ETL is complete and the graph is populated, our test suite will execute `/app/verify_performance.py`. 
This verifier measures the execution time of `/home/user/target_query.cypher` across 50 iterations. 
- To pass, your graph query must yield the correct most frequent path AND the average query runtime must be strictly **< 15 milliseconds**. (Without proper graph indexes and materialization logic, it will take > 200ms).

Run `/app/start_services.sh` to initialize the databases and populate the initial 50,000 rows in Postgres before you begin.