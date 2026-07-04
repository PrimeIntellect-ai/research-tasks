You are a data analyst and C developer working on a custom, high-performance in-memory graph database for analyzing a Knowledge Graph exported as CSV files.

You have been provided with two CSV files in `/home/user/data/`:
1. `nodes.csv` (columns: `node_id`, `node_type`)
2. `edges.csv` (columns: `src_id`, `dst_id`, `relation_type`)

Your task is to write a web service in **C** that loads these CSV files into memory and answers analytical queries over HTTP. 

Additionally, your team previously used a proprietary scoring algorithm to compute a node's "Influence Score". The source code is lost, but the compiled binary remains at `/app/kg_oracle`. It takes three arguments: the path to `edges.csv`, the path to `nodes.csv`, and a `node_id`. It prints a single integer score. For performance reasons, your new C service must *not* shell out to this binary. Instead, you must reverse-engineer the logic used by `/app/kg_oracle` (by treating it as a black box and observing its outputs for various nodes) and natively implement the identical scoring logic in your C program.

Write a C program (e.g., `server.c`) that starts an HTTP server listening on `127.0.0.1:9090`. You may use standard libraries, raw sockets, or install a lightweight library like `libmicrohttpd` using `sudo apt-get` (assume you have passwordless sudo for package installation if needed, though raw sockets or standard user-space libraries are preferred).

Your service must implement the following HTTP GET endpoints:

1. `GET /pattern?src_type=<TYPE1>&dst_type=<TYPE2>&rel=<REL>`
   Finds all matching subgraphs. 
   **Response format:** A JSON array of arrays, where each inner array contains the string IDs: `[["src_id_1", "dst_id_1"], ["src_id_2", "dst_id_2"]]`. Order does not matter. Return a `200 OK` with `Content-Type: application/json`.

2. `GET /influence?node=<ID>`
   Calculates the proprietary Influence Score for the given node, matching the exact logic of `/app/kg_oracle`.
   **Response format:** A JSON object: `{"node": "ID", "score": <integer>}`.

**Constraints & Instructions:**
- Compile your program to `/home/user/graph_server`.
- Run the server in the background so the verifier can test it.
- Write any server logs or initialization output to `/home/user/server.log`. Make sure to print "SERVER READY" to this log file once the CSVs are fully loaded and the port is bound.
- The C code must be robust enough to handle the provided dataset.
- Be precise with your JSON formatting.