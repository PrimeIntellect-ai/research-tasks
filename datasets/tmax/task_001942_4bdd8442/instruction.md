You are an AI assistant helping a database administrator optimize a network routing query system. 

We have a legacy network routing database stored at `/home/user/network.db` (SQLite3). It contains two tables detailing our infrastructure: `routers` and `links`. We don't have the exact schema documentation, so you will need to analyze the database to understand the relationships.

Additionally, link traversal costs in our network are dynamically calculated by an old, undocumented binary located at `/app/link_cost_oracle`. This binary is stripped, but we know its usage: running `/app/link_cost_oracle <source_id> <target_id>` outputs a single integer representing the cost to traverse the link from `source_id` to `target_id`.

Your task is to build a modern Python HTTP REST API that replaces our legacy query interface. You can use frameworks like Flask or FastAPI. The service must run in the background, bind exactly to `127.0.0.1:9000`, and implement the following specification:

**Authentication:**
All endpoints must require an `Authorization: Bearer ADMIN_TOKEN_99` header. Return a 401 Unauthorized status code if this is missing or incorrect.

**Endpoint 1: Result Pagination & Filtering**
`GET /routers?tier=<tier_string>&limit=<int>&offset=<int>`
- Filter the routers by their `tier` column.
- Sort the resulting routers by their `id` in strictly **descending** order.
- Apply the `limit` and `offset` for pagination.
- Return JSON in this format: `{"data": [{"id": 10, "name": "r10", "tier": "edge"}, ...]}`

**Endpoint 2: Graph Traversal & Shortest Path**
`GET /route?start=<start_id>&end=<end_id>`
- Traverse the graph defined by the `links` table in the database to find the shortest path from `start_id` to `end_id`.
- The "cost" of each link must be computed dynamically by invoking the `/app/link_cost_oracle` binary. You must minimize the total sum of these costs.
- The path should be returned as an ordered list of router IDs (including start and end).
- Return JSON in this exact format: `{"path": [1, 5, 8, 12], "total_cost": 45}`
- If no path exists, return a 404 status code with `{"error": "No path found"}`.

**Instructions:**
1. Analyze the SQLite database at `/home/user/network.db`.
2. Write your Python API server. Ensure it uses the `/app/link_cost_oracle` to get edge weights.
3. Start the server so it listens continuously on `127.0.0.1:9000`. Leave it running so our automated test suite can query it. 
4. You may write your server script to `/home/user/api_server.py` and run it in the background (`python3 /home/user/api_server.py &`).