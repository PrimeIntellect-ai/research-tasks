You are a data engineer building an ETL pipeline to analyze a microservices dependency knowledge graph. 

We have a raw dataset representing various relationships between services, databases, and infrastructure components. This data is located at `/home/user/data/kg_triples.tsv`. It is a Tab-Separated Values (TSV) file with three columns: `Source_Node`, `Relationship_Type`, and `Target_Node`.

Your task is to build a toolchain that finds the shortest dependency chain between two specific services. 

Specifically, you need to do the following:
1. Write a C++ program located at `/home/user/etl/graph_solver.cpp`. This program should:
   - Take three command-line arguments: the input TSV file path, the start node, and the end node.
   - Parse the TSV file, keeping *only* the edges where the `Relationship_Type` is exactly `depends_on`. Treat the edges as directed (Source_Node -> Target_Node).
   - Compute the shortest path between the start node and the end node using Breadth-First Search (BFS).
   - Output the result to a file located at `/home/user/output/shortest_path.txt`.

2. The output file `/home/user/output/shortest_path.txt` must have exactly the following format (including exact case and spacing):
   ```
   Length: <number_of_edges>
   Path: <Node1> -> <Node2> -> ... -> <NodeN>
   ```
   If no path exists, the file should contain exactly `No path found.`.

3. Create a bash script located at `/home/user/etl/pipeline.sh`. This script must:
   - Compile the C++ program using `g++` into an executable named `/home/user/etl/graph_solver`. Require C++17 (`-std=c++17`).
   - Run the compiled executable, specifying `/home/user/data/kg_triples.tsv` as the input, `API_Gateway` as the start node, and `Storage_Cluster_9` as the end node.

Make sure the bash script is executable.

Constraints:
- You must write the solution in C++.
- Use standard C++ libraries (e.g., `<iostream>`, `<fstream>`, `<vector>`, `<string>`, `<unordered_map>`, `<queue>`). No external libraries (like Boost) are needed or allowed.