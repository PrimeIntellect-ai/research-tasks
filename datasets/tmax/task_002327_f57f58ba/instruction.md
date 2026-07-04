You are a database administrator tasked with optimizing and deploying a custom C++ graph database engine. 

We have a vendored graph database package located at `/app/vendored/simple-graph-db`. It provides a lightweight HTTP server for querying graph analytics (specifically, node centrality). We need to get this service up and running to serve a new application, but it has a few problems:

1. **Compilation Error**: The package currently fails to build. The original developer left a deliberate error in the `Makefile`. You will need to fix this (hint: check the C++ standard being used versus what the code requires).
2. **Pagination Bug**: The HTTP endpoint `/api/top_centrality` accepts `limit` and `offset` query parameters. However, the `offset` parameter is currently ignored in the query pipeline logic located in `src/query_handler.cpp`. You must fix the C++ code so that it properly slices the sorted result set using both `offset` and `limit`. Make sure you handle bounds checking appropriately so the server doesn't crash if the offset exceeds the number of nodes.
3. **Deployment**: Once fixed, compile the engine using `make`. Then, start the server so that it listens on `127.0.0.1` port `8080`. You must load the graph dataset located at `/app/data/edges.csv` by passing it via the `--graph` command-line argument.
   
Example of how the server is expected to be run:
`./build/graph_server --port 8080 --graph /app/data/edges.csv`

Please leave the server running in the background once you have fixed the code, compiled it, and verified it works. The automated verification system will send real HTTP requests to your server to ensure pagination is working correctly and the correct top nodes are returned.

Requirements:
- Do not move the vendored package out of `/app/vendored/simple-graph-db`.
- The server must bind to `127.0.0.1:8080`.
- Return the results in the exact JSON format the server currently uses.