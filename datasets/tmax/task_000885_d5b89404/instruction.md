You are acting as a data analyst dealing with complex graph data exported as CSV files. You have been given a proprietary, stripped binary tool located at `/app/query_engine` which performs high-speed graph traversals. 

Your objective is to build a high-performance integration layer in **C** that exposes this engine as a network service to internal NoSQL aggregation pipelines.

**Requirements:**
1. **Analyze the Binary:** The binary `/app/query_engine` processes graph data, but documentation is missing. Use reverse-engineering tools (like `strings`, `ltrace`, or `strace`) to figure out how it takes inputs (e.g., arguments, environment variables, or standard input) and what format it expects for its Cypher-like traversal syntax.
2. **Graph Data:** A dataset is located at `/home/user/data/edges.csv`. The file has no header. Each line is formatted as `SourceNode,TargetNode,Weight`. 
3. **C Network Service:** Write a C program at `/home/user/server.c` and compile it to `/home/user/server`. 
   - The server must listen on TCP port `127.0.0.1:9090`.
   - It should accept incoming connections and read a single line of NoSQL-style JSON per request, exactly matching this format: `{"start_node": "<NODE_ID>", "max_hops": <INTEGER>}\n`
   - For each request, the C server must translate this JSON into the specific graph query language syntax the binary expects, invoke the `/app/query_engine` binary, capture its standard output, and convert the raw results into a JSON array of reachable nodes (e.g., `["NodeB", "NodeC"]`).
   - Send the JSON array back to the TCP client, terminated by a newline (`\n`), and close the connection.
4. **Execution:** Keep your server running in the background on port `9090` so that automated verification can test it with several requests.

Ensure your C code handles basic string manipulation and process forking correctly. Do not hardcode the expected answers; your server must dynamically use the binary to answer the queries.