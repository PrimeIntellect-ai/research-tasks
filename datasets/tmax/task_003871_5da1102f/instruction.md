You are a database administrator and data engineer optimizing a slow analytics pipeline. 

We have a custom graph database engine that exports data as JSONL files. Recently, an analyst wrote a query to find a specific pattern: pairs of users who know each other and have both bought the same product. 

Unfortunately, the query engine evaluates this pattern by doing an implicit cross join on the `BOUGHT` relationship (finding all user pairs who bought a product, and then checking if they know each other). As the dataset grows, this O(N^2) operation per product is destroying our processing times.

You are provided with a reference implementation of the current query engine at `/app/ref_engine`. It is a stripped binary that takes no arguments. When executed, it reads `/app/data/nodes.jsonl` and `/app/data/edges.jsonl` from the current working directory and outputs the results to `results.csv`. 

Your task is to write a highly optimized Go program that executes this exact same logical query but utilizes efficient in-memory hash joins and adjacency lists (i.e., avoiding the cross join) to process the data in O(E + V) time.

Requirements:
1. The input dataset is located at `/app/data/nodes.jsonl` and `/app/data/edges.jsonl`.
    * Nodes have the format: `{"id": "node_id", "type": "User|Product"}`
    * Edges have the format: `{"src": "node_id", "dst": "node_id", "rel": "KNOWS|BOUGHT"}`
    * Note: `KNOWS` is technically directed in the data, but for this query, it must be treated as **undirected** (if A knows B, B knows A). `BOUGHT` is directed (User -> Product).
2. Write a Go program at `/home/user/fast_query.go` and compile it to `/home/user/fast_query`.
3. Your program must output exactly the same data as `/app/ref_engine`, to a file named `/home/user/results.csv`. 
4. The output must be a standard CSV file with the header `User1,User2,Product`. 
5. Each matching triangle `(U1, U2, P)` should only be printed once per pair of users. To ensure deterministic output, ensure that `User1` is lexicographically less than `User2` in the output row. The entire CSV file must be sorted lexicographically by `Product`, then `User1`, then `User2`.
6. Your Go implementation must achieve at least a **10x runtime speedup** compared to `/app/ref_engine`. 

Use `go run` or `go build` to iterate. You can run `/app/ref_engine` to inspect its exact output format and verify your results against it.