You are tasked with fixing and optimizing a simple Bash-based API server that interacts with a graph database. 

We have a custom HTTP server written entirely in Bash (`/home/user/graph_api.sh`) that serves requests on `127.0.0.1:9000`. It receives requests in the format `GET /path?start=<node_id>&end=<node_id> HTTP/1.1` and is supposed to return the shortest path between the two nodes querying an SQLite database located at `/home/user/graph.db`.

However, the current implementation has several severe issues:
1. The SQL query embedded in the bash script uses an implicit cross join when trying to traverse the graph, returning completely wrong paths and path costs.
2. The server crashes on parameterized query construction due to improper parsing of the URL parameters.

Your objectives:
1. Modify `/home/user/graph_api.sh` to correctly parse the `start` and `end` URL parameters from the incoming HTTP request.
2. Rewrite the SQLite query inside the bash script using a correct Recursive Common Table Expression (CTE) to compute the actual shortest path between `start` and `end`.
3. The HTTP response must return a 200 OK status code with a JSON payload containing the exact shortest path and its total cost.
4. To ensure your JSON payload format and path logic are correct, we have provided a stripped, black-box binary at `/app/path_oracle`. You can execute it natively via `/app/path_oracle <start_node> <end_node>` to see the exact canonical JSON output format expected by the clients.
5. Start your fixed server so it listens on `127.0.0.1:9000` and leave it running in the background.

The database `/home/user/graph.db` has a single table:
`edges (source TEXT, target TEXT, weight INTEGER)`

Example:
If a client sends `GET /path?start=A&end=D HTTP/1.1`, your server should execute the optimized recursive query, format the output to perfectly match what `/app/path_oracle A D` outputs, and return it as the HTTP response body.

Ensure the server stays running and can handle multiple sequential requests. You must use only Bash built-ins, standard coreutils, `nc`/`socat`, and `sqlite3`.