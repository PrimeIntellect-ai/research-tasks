You are acting as a data analyst. You have been provided with two CSV files representing a property graph export: `/home/user/nodes.csv` and `/home/user/edges.csv`.

Recently, our graph database index became corrupted, and the export tool dumped stale/duplicate edges into `edges.csv`. The file has the header `src,dst,weight,timestamp`. If there are multiple edges between the same `src` and `dst`, only the one with the highest `timestamp` is valid; the rest are stale and must be ignored. 

The `nodes.csv` file has the header `id,name`.

Your task is to write a C++ program at `/home/user/graph_solver.cpp` that:
1. Reverses the corrupted data model by parsing the CSV files and ignoring stale edges (keeping only the most recent edge for any directional `src` -> `dst` pair).
2. Models the data as a directed graph.
3. Finds the shortest path (lowest total weight) from the node with the name "START" to the node with the name "END".
4. Exports the resulting path to `/home/user/path.csv` with the exact header `step,node_id,node_name,cumulative_weight`. 

`step` should start at 0 for the START node. `cumulative_weight` should be 0 for the first step, and increase by the valid edge weight for each subsequent step.

Compile your C++ program using `g++ -O3 -std=c++17 /home/user/graph_solver.cpp -o /home/user/graph_solver` and execute it to generate `/home/user/path.csv`.