You are a database administrator tasked with optimizing a graph database query. We have a custom graph engine that stores network topology data in a plain CSV file. Recently, queries to find the shortest path between network nodes have been timing out.

The data model is stored at `/home/user/graph_db/edges.csv`. The file is headerless and contains comma-separated values representing a directed graph. You need to reverse engineer its basic schema (it represents Source, Destination, and Cost).

Your task is to write a highly optimized C++ program that replaces our old, inefficient query plan. 

Requirements:
1. Analyze `/home/user/graph_db/edges.csv` to understand the data.
2. Write a C++ program named `/home/user/graph_db/fast_query.cpp`.
3. The program must implement an optimal graph traversal algorithm (e.g., Dijkstra's using a priority queue) to find the shortest path from node `10` to node `500`.
4. The program must read `edges.csv` dynamically.
5. Compile your program to `/home/user/graph_db/fast_query` using standard `g++`.
6. Run your program and write the exact output to `/home/user/graph_db/result.log`.

The output in `/home/user/graph_db/result.log` must be formatted exactly like this (with the correct cost and sequence):
```
Cost: [TOTAL_COST]
Path: 10 -> [NODE] -> [NODE] -> 500
```
If there are multiple paths with the exact same minimum cost, any of the shortest paths is acceptable.