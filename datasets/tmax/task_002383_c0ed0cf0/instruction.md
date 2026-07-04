I need your help fixing a data analysis issue and replacing an old black-box binary with a new microservice. 

I am a data analyst working with two datasets:
- `/home/user/data/hierarchy.csv`: Contains `parent_id,child_id` representing a directed graph (a tree/forest of nodes).
- `/home/user/data/values.csv`: Contains `node_id,value` representing an integer metric for each node.

We have a legacy compiled tool at `/app/legacy_engine`. It's a stripped, undocumented binary. When you run `/app/legacy_engine <node_id>`, it outputs the exact aggregated value for that node. The logic it uses is to find the node and *all of its recursive descendants*, then sum up all their values. 

I tried writing a SQL query to do this using standard joins, but I accidentally created an implicit cross join and the values exploded. I need you to build a correct, robust implementation.

Your task is to create a Rust-based HTTP microservice that calculates this correctly.
Requirements:
1. Initialize a new Rust project at `/home/user/aggregate_service` and implement the server. You can use standard crates like `axum`, `tokio`, `rusqlite` (with SQLite's `WITH RECURSIVE`), or simply parse the CSVs into memory.
2. The service MUST listen exactly on `127.0.0.1:8080`.
3. It must expose a `GET /aggregate/{node_id}` endpoint.
4. The endpoint MUST require an `Authorization` header with the exact value `Bearer analyst_token_99`.
5. The endpoint should return a 200 OK with a JSON payload in this exact format: `{"node": {node_id}, "total_value": {calculated_sum}}`.
6. You can use `/app/legacy_engine` as an oracle to reverse-engineer or verify your recursive aggregation logic for any test node.

Start the service in the background once you are done so my automated tools can query it.