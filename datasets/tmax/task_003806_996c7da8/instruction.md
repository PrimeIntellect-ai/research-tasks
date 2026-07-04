You are an expert data analyst and systems engineer. We have a set of hierarchical supply chain data in CSV format, but our legacy tools cannot perform recursive graph queries on it. 

You need to deploy a standalone graph querying service in Rust to process these CSVs and respond to dynamic queries.

Here are the requirements:
1. **Data Model**: There are two CSV files located at `/home/user/data/nodes.csv` (columns: `id`, `name`, `type`) and `/home/user/data/edges.csv` (columns: `parent_id`, `child_id`, `weight`). 
2. **Vendored Engine**: We have a pre-vendored Rust graph engine located at `/app/vendored/graph-engine-0.4.2/`. However, it currently crashes when executing recursive hierarchical queries due to a known bug in how it resolves recursive parameter bounds. You must locate the broken configuration or bug within its source code and fix it without accessing the internet.
3. **HTTP Service Integration**: Write a Rust server using only standard libraries (or the provided local engine) that loads the CSV data using the fixed engine. 
4. **Network Protocol**: The server must bind exactly to `127.0.0.1:9090`. It must expose an HTTP POST endpoint at `/query`.
5. **Authentication**: All requests to `/query` must require an `Authorization` header with the exact value `Bearer sc-analytics-2024`. Reject any other requests with a 401 status code.
6. **Query Execution**: The endpoint must accept JSON payloads in the format `{"start_node": "A1", "max_depth": 3}`. Using the vendored engine's recursive query builder, calculate the total downstream weight from the `start_node` up to `max_depth`. The response must be a JSON object: `{"result": <integer>}`.

Ensure your service is left running in the background so our verification suite can test it. Write any logs to `/home/user/service.log`. Do not use external network resources to download new crates.