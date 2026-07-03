You are a data engineer building a lightweight ETL pipeline step to extract knowledge graph patterns. 

You have been provided with two CSV files representing a local graph database dump:
1. `/home/user/graph_nodes.csv` - Contains node definitions. Header: `id,type`
2. `/home/user/graph_edges.csv` - Contains edge definitions. Header: `source,target,relation,weight`

Your task is to write and execute a Go program (`/home/user/extract_patterns.go`) that performs an in-memory graph traversal to find a specific pattern, simulating a knowledge graph query with result sorting and pagination.

The pattern to find is a path of length 2: `(A) -[follows]-> (B) -[likes]-> (C)`
Where:
- Node `A` is of type `Bot`
- Node `B` is of type `User`
- Node `C` is of type `Post`

For every valid path found, calculate the `total_weight` as the sum of the weight of the `follows` edge and the `likes` edge.

Your Go program must:
1. Parse the CSV files and build efficient in-memory lookup maps (indexing strategy) to quickly find nodes by type and out-edges by source.
2. Traverse the graph to find all paths matching the exact criteria above.
3. Sort the resulting paths by `total_weight` in strictly descending order. If there is a tie, sort by `A.id` ascending, then `B.id` ascending.
4. Paginate/Filter the results to keep ONLY the top 3 paths.
5. Output the top 3 paths to `/home/user/top_patterns.json` as a JSON array of objects.

The output JSON array must have exactly this format:
```json
[
  {
    "bot_id": "...",
    "user_id": "...",
    "post_id": "...",
    "total_weight": 1.5
  }
]
```

Write the Go code, run it, and ensure the `/home/user/top_patterns.json` file is correctly generated. You can use standard Go library packages only.