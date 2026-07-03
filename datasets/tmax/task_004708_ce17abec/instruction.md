You are a Data Engineer building out an ETL and reporting pipeline. We have a lightweight reporting service built entirely in Bash and PostgreSQL that serves hierarchical employee data. 

Currently, the service is broken. Our `/app/start.sh` script brings up PostgreSQL and a bash-based HTTP server using `socat`. However, when querying the API for an employee's subordinates, the underlying SQL query contains a severe bug (an implicit cross join) that causes it to return incorrect, duplicated results and hang the server. Furthermore, the database is missing crucial indexes for hierarchical traversal.

Your objectives:

1. **Fix the API Server:**
   The start script `/app/start.sh` brings up PostgreSQL but the `socat` server in `/app/server.sh` is crashing or returning invalid HTTP headers. Fix `/app/server.sh` and `/app/handle_req.sh` so that it correctly parses a `GET /api/subordinates?manager_id=<id>` request and returns a valid HTTP 200 response with a JSON array of subordinate objects. The server must listen on `0.0.0.0:8080`.

2. **Fix the Recursive Query:**
   The file `/app/query.sql` is currently written with a flawed cross join. Rewrite it to use a proper `WITH RECURSIVE` Common Table Expression (CTE). The query should return the `id`, `name`, and `depth` (integer, where the queried manager is depth 0, their direct reports are depth 1, etc.) of the manager and ALL their direct and indirect subordinates. 

3. **Optimize the Database:**
   The `employees` table in the `company` database has columns `id`, `name`, and `manager_id`. Traversing this graph is slow. Create a new SQL script at `/app/optimize.sql` that creates an index named `idx_manager_id` on the `manager_id` column. Run this script against the `company` database.

4. **Coordinate the Services:**
   Ensure `/app/start.sh` successfully starts PostgreSQL, waits for it to be ready, applies `/app/optimize.sql`, and starts the `socat` HTTP server in the background. 

The automated test will:
- Execute `/app/start.sh`.
- Verify the PostgreSQL execution plan uses `idx_manager_id`.
- Make an HTTP GET request to `http://127.0.0.0:8080/api/subordinates?manager_id=1` and expect a correctly formatted JSON array containing the manager and all recursive subordinates.