You are a database administrator tasked with optimizing queries for a microservices architecture. A recent graph database query dumped its raw execution results into a CSV file located at `/home/user/graph_dump.csv`. 

This file contains an edge list representing network latency between different service nodes, with the following columns:
`src_id,src_type,dst_id,dst_type,latency_ms`

You need to write a Python script to process this result dump to accomplish two goals:
1. **Reverse-engineer the schema:** Determine all unique directional relationships between service *types* (e.g., if there is an edge from a 'Gateway' node to an 'App' node, the schema contains `Gateway -> App`).
2. **Compute the shortest path:** Calculate the shortest path (minimum total latency) from the node `Gateway_Alpha` to the node `DB_Omega`.

You may only use Python standard libraries. 

Save your final results to exactly `/home/user/optimization_report.txt` with the following strict format:

```
SCHEMA:
[Sorted list of unique type relationships, one per line, format: SourceType -> DestType]

SHORTEST_PATH_LATENCY: [Total latency integer]
SHORTEST_PATH: [Node1 -> Node2 -> Node3 ...]
```

For example:
```
SCHEMA:
App -> Cache
App -> DB
Cache -> DB
Gateway -> App

SHORTEST_PATH_LATENCY: 45
SHORTEST_PATH: Gateway_Alpha -> App_1 -> Cache_1 -> DB_Omega
```

Make sure the SCHEMA list is sorted alphabetically by the `SourceType`, and then by `DestType` in case of ties.