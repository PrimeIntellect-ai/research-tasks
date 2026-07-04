You are a database administrator tasked with optimizing and extracting insights from a hybrid logistics data system. The data is split between a relational database (`/home/user/logistics.db`) and a document dump of telemetry events (`/home/user/events.jsonl`).

You need to perform three specific operations and save the results in precise formats.

**Phase 1: Relational Query Optimization (Complex Joins & Query Plans)**
The `logistics.db` SQLite database has three tables:
- `hubs` (`id` INTEGER, `name` TEXT)
- `routes` (`id` INTEGER, `src_hub` INTEGER, `dst_hub` INTEGER, `distance` REAL)
- `deliveries` (`id` INTEGER, `route_id` INTEGER, `duration_hours` REAL)

A critical query is running slow. The query aims to find the names of the source and destination hubs, and the `duration_hours` for all deliveries that took longer than 100 hours.
1. Formulate this query (joining `deliveries`, `routes`, and `hubs` twice for src and dst).
2. Create the optimal index(es) in the database to speed up filtering on `duration_hours`.
3. Output the exact `EXPLAIN QUERY PLAN` for your optimized query into `/home/user/query_plan.txt`. (Do not change the default output format of sqlite3).

**Phase 2: Document Aggregation (NoSQL-style Pipeline)**
The `/home/user/events.jsonl` file contains JSON objects representing telemetry events at various hubs. Each line has the format: `{"hub_id": INT, "event": "processing", "time_spent": FLOAT}`.
1. Parse this file and calculate the average `time_spent` for each `hub_id`.
2. Identify all hubs where the average `time_spent` is strictly greater than `10.0`.
3. Save these "slow hubs" to `/home/user/slow_hubs.csv` in the format `hub_id,avg_time_spent` (sorted numerically by `hub_id` ascending, average time rounded to 2 decimal places).

**Phase 3: Graph Projection & Materialization**
We want to project a graph of the network where congestion is highest.
1. Extract the network topology from `logistics.db` (`routes` table).
2. Filter the routes to create a subgraph containing ONLY edges (routes) where BOTH the `src_hub` and `dst_hub` are present in the "slow hubs" list generated in Phase 2.
3. Save this graph projection as an edge list to `/home/user/slow_graph.csv` in the format `src_hub,dst_hub,distance` (sorted by `src_hub` then `dst_hub` ascending).

Use standard command-line tools (sqlite3, jq, python3, awk, bash, etc.) to complete this task.