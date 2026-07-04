You are a research assistant tasked with organizing and analyzing a citation dataset. 

I have a raw dataset of citation edges in a CSV file located at `/home/user/dataset/citations.csv`. We previously tried loading this into an SQLite database, but the indices got corrupted and returned stale rows, so we are starting over from the raw CSV.

Your task consists of the following phases:
1. **Database Initialization & Index Strategy**: 
   Create a new SQLite database at `/home/user/dataset/graph.db`. Create a table named `citations` with columns `source` (INTEGER) and `target` (INTEGER). Load the data from `citations.csv` into this table. Design and create an optimal index (or indices) to speed up queries that frequently look up the `target` given a `source`, as well as queries checking if a specific `(source, target)` pair exists.

2. **Graph Conversion & Traversal**:
   Write a Python script (using standard libraries and `networkx`) to read the verified data directly from your newly created SQLite database. Construct a directed graph from the citation edges.
   
3. **Shortest Path Computation**:
   Compute the shortest path from node `10` to node `99` in the directed graph.

4. **Result Export**:
   Export the exact sequence of nodes in the shortest path as a comma-separated string (e.g., `10,45,67,99`) and save it to exactly `/home/user/dataset/shortest_path.txt`.

Please execute the necessary shell commands and write the Python scripts required to complete this task. You can install `networkx` via pip if it is not already installed.