You are a database administrator and backend engineer tasked with optimizing a hybrid relational-graph database and exposing a secure query API.

We have a vendored query engine located at `/app/hyperquery` that translates high-level graph and NoSQL-style document queries into parameterized SQLite SQL. This package is currently broken and not connecting to our database correctly.

Your objectives:

1. **Fix the Vendored Package**:
   The `/app/hyperquery` library is supposed to read the target database path from the `HYPER_DB_PATH` environment variable, but due to a typo or logical error introduced in its last patch, it always connects to an in-memory database and drops data. Inspect and fix the source code in `/app/hyperquery` so it correctly respects the `HYPER_DB_PATH` environment variable.

2. **Index Strategy Design**:
   You have a SQLite database located at `/home/user/graph_data.db`. It contains two tables simulating a property graph:
   - `nodes (id TEXT PRIMARY KEY, labels TEXT, properties JSON)`
   - `edges (source TEXT, target TEXT, rel_type TEXT, properties JSON)`
   
   Queries filtering by the `rel_type` and joining `source` to `target` are currently resulting in full table scans. Furthermore, NoSQL aggregation pipelines filtering on the JSON field `$.category` inside the `nodes` table are extremely slow.
   
   Write a SQL script at `/home/user/optimize.sql` containing the optimal `CREATE INDEX` statements to speed up:
   a) Graph traversals traversing `edges` by `source` and `rel_type`.
   b) Graph traversals traversing `edges` by `target` and `rel_type`.
   c) Document retrieval filtering by the JSON property `category` (e.g., `json_extract(properties, '$.category')`).
   Apply these indexes to `/home/user/graph_data.db`.

3. **Multi-Protocol API Implementation**:
   Write a Python HTTP server script at `/home/user/server.py` using only the standard library (`http.server`, `json`, `sqlite3`, etc.). The server must:
   - Listen exactly on `127.0.0.1:8080`.
   - Accept `POST` requests at the `/api/query` endpoint.
   - Require an `Authorization` header with the exact value `Bearer super-secret-dba-token`. Return 401 Unauthorized if missing or incorrect.
   - Accept a JSON body with the schema: `{"query": "<raw_sql_query>", "params": [<list_of_parameters>]}`.
   - Use the fixed `/app/hyperquery` package (which wraps `sqlite3`) to execute the parameterized query securely against `/home/user/graph_data.db`. You can import it via `import sys; sys.path.append('/app'); import hyperquery.engine`. Use its `execute_query(query_string, params_list)` function.
   - Return an HTTP 200 response with a JSON array of the fetched rows.
   - Return an HTTP 400 response with `{"error": "Invalid payload"}` if the JSON is malformed.

Leave your `server.py` running in the background or be prepared for an automated verifier to execute it and test the HTTP protocol constraints, database reads, and query optimizations.