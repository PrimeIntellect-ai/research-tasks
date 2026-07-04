You are an integration developer working on a system that orchestrates interdependent services. You have been provided with a Protobuf schema defining a dependency graph, and a serialized binary payload containing the graph data.

Your task is to write a script to deserialize the payload and determine the correct execution order of the services.

Files provided:
1. `/home/user/graph.proto`: A Protobuf definition containing a `Graph` message and a `Node` message.
2. `/home/user/graph_data.bin`: A serialized binary file containing a single `Graph` message.

Steps:
1. Compile the `/home/user/graph.proto` file for Python. You may install any necessary protobuf tools (e.g., `grpcio-tools`, `protobuf`) using `pip`.
2. Write a Python script (e.g., `/home/user/resolve.py`) that reads `/home/user/graph_data.bin` and parses it into a `Graph` message.
3. The graph contains a list of nodes, each with an `id` and a `depends_on` list of node IDs. Perform a topological sort to determine the execution order.
4. **Sorting Rules:** 
   - A node can only be executed (added to the order) once all the nodes in its `depends_on` list have been executed.
   - If multiple nodes are available to be executed at the same time, always pick the node with the alphabetically smallest `id` first (tie-breaker).
5. Write the final execution order of the node IDs as a comma-separated string (no spaces, e.g., `A,B,C`) to `/home/user/order.txt`.

Ensure your python script executes successfully and generates the `/home/user/order.txt` file.