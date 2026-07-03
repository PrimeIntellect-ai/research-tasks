You are acting as a database administrator. We are migrating our result processing and graph materialization pipeline. Currently, we rely on a proprietary, compiled binary utility located at `/app/graph_materializer_bin` to project our relational database (`/home/user/data.db`) into a graph format. 

This binary takes a JSON document representing a graph projection query as standard input and outputs a materialized list of edges to standard output in CSV format. 

Unfortunately, the original source code for this binary is lost. We know it maps relational tables (Users, Departments, Roles, Projects) into a graph representation based on the JSON configuration, but naive attempts to recreate it in SQL have resulted in implicit cross-joins and wildly incorrect edge counts.

Your task is to write a Python 3 script at `/home/user/project_graph.py` that completely replaces this binary. 
It must:
1. Accept the exact same JSON configuration format via standard input.
2. Connect to the SQLite database at `/home/user/data.db`.
3. Perform the correct cross-representation mapping (relational tables to graph edges) without falling into the implicit cross-join trap.
4. Print the exact same materialized graph edge list (CSV format: `source_node,target_node,edge_type`) to standard output as the `/app/graph_materializer_bin` does.

You can interact with the binary to reverse-engineer its behavior and understand the exact projection logic. You can use standard tools like `objdump`, `strings`, or simply treat it as a black box and send it various test JSON payloads to see how it constructs the graph.

Ensure your Python script's output is bit-for-bit identical to the binary's output for any valid graph projection JSON document. Your script must be executable like so: `cat query.json | python3 /home/user/project_graph.py`.