You are a database administrator tasked with optimizing and migrating querying logic. We have a relational tabular representation of a network graph that needs to be queried for the shortest path and mapped into a document representation (JSON) for a downstream NoSQL database.

Your task is to write a C++ program that reads a relational edge list from a CSV file, computes the shortest path using graph traversal, and outputs the result as a JSON document.

Here are the specific requirements:
1. Read the input file located at `/home/user/edges.csv`. This file has a header `source,target,weight` and contains directed edges.
2. Build an internal graph representation and use Dijkstra's algorithm (or another shortest path graph traversal algorithm) to find the shortest path from node `A` to node `Z`.
3. Map the result into a document format and output it to `/home/user/output.json`.
4. The JSON must exactly follow this structure:
   ```json
   {
     "path": ["A", "node1", "node2", "Z"],
     "total_weight": 15
   }
   ```
5. Create your C++ source file at `/home/user/shortest_path.cpp`.
6. Compile your program (e.g., `g++ -O3 /home/user/shortest_path.cpp -o /home/user/shortest_path`) and run it so that `/home/user/output.json` is generated.

Do not use any external libraries other than the C++ Standard Library.