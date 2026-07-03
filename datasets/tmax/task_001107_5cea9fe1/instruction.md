You are an AI assistant helping a researcher organize and query a large knowledge graph dataset. The dataset is stored in a SQLite database located at `/home/user/dataset.db`, containing research papers, authors, and concepts. 

The researcher has also provided a proprietary, compiled binary utility at `/app/path_scorer` that evaluates the "relevance score" of any given path through the knowledge graph. 

Your task is to build and run a Go-based HTTP REST API that allows querying this graph and evaluating paths using the provided binary.

**Requirements:**

1. **Database Schema:**
   The SQLite database `/home/user/dataset.db` has two tables:
   - `nodes` (`id` TEXT PRIMARY KEY, `label` TEXT, `name` TEXT)
   - `edges` (`source` TEXT, `target` TEXT, `relation` TEXT) - where `source` and `target` map to node `id`s.

2. **The Scoring Binary:**
   - Location: `/app/path_scorer` (it is a stripped, black-box binary).
   - Usage: It accepts a space-separated list of node IDs as command-line arguments and prints a single floating-point score to stdout. 
   - Example: `/app/path_scorer n10 n45 n2` outputs `0.854`.

3. **API Specification:**
   You must write a Go web server (save the source to `/home/user/server.go`) that listens on `127.0.0.1:9090` and implements the following endpoints:

   **Endpoint A: `GET /nodes`**
   - **Query Parameters:**
     - `label` (string, required): Filter nodes by this exact label (e.g., `Author`).
     - `limit` (integer, required): Maximum number of results to return.
     - `page` (integer, required): 1-indexed page number for pagination.
   - **Behavior:** Query the database using properly parameterized SQL. Sort the results alphabetically by `id` ascending.
   - **Response Format (200 OK):**
     ```json
     {
       "page": 1,
       "limit": 10,
       "results": [
         {"id": "a1", "name": "Alice Smith"},
         {"id": "a2", "name": "Bob Jones"}
       ]
     }
     ```

   **Endpoint B: `GET /shortest-path`**
   - **Query Parameters:**
     - `start` (string, required): Starting node `id`.
     - `end` (string, required): Ending node `id`.
   - **Behavior:** 
     - Compute the shortest path between the `start` and `end` nodes in the graph (treating edges as unweighted and undirected). If multiple paths have the same minimum length, return any one of them.
     - Invoke the `/app/path_scorer` binary, passing the ordered sequence of node IDs in the computed path as arguments.
   - **Response Format (200 OK):**
     ```json
     {
       "path": ["start_node", "intermediate_node", "end_node"],
       "score": 0.854
     }
     ```
     If no path exists, return a 404 with `{"error": "no path found"}`.

4. **Execution:**
   - Compile and run your server.
   - You must leave the server running in the background on port `9090` before concluding your turn (e.g., using `nohup go run /home/user/server.go &`). Ensure it has fully started and is accepting connections.

Use standard Go libraries (like `net/http` and `database/sql` with `github.com/mattn/go-sqlite3`). The dataset size is small enough (~1000 nodes) that loading the graph into memory for traversal is acceptable, or you can query it recursively.