You are a data analyst troubleshooting a network routing dataset. We have a CSV file located at `/home/user/network.csv` containing historical network link data. The file contains records of directed edges with their latency and reliability scores at various timestamps.

However, the dataset contains "stale" rows because the network logging system appends new metrics for an edge instead of updating them. 

Your task is to write a C++ program (which you should save and compile at `/home/user/solve.cpp`) to compute the shortest path (lowest total latency) from node `S` to node `T`.

Before computing the path, you must correctly process the graph data:
1. For any given directed edge (from `source` to `target`), there may be multiple rows with different `timestamp` values. You must ONLY consider the row with the maximum `timestamp` for that specific edge.
2. After isolating the latest row for each edge, you must filter out any edges where the `reliability_score` is strictly less than `0.8`. If the latest row for an edge has a reliability score < 0.8, that edge is considered down and cannot be used at all.

Using only the valid, up-to-date edges, find the shortest path by `latency` from `S` to `T`. 

Write the output to a file named `/home/user/shortest_path.txt` in exactly this format:
```
Latency: <total_latency>
Path: <node1>,<node2>,...,<nodeN>
```
For example:
```
Latency: 45
Path: S,X,Y,T
```

Ensure your C++ code can be compiled with `g++ -O2 /home/user/solve.cpp -o /home/user/solve` and runs successfully.