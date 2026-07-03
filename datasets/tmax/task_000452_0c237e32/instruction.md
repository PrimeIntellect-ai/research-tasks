You are a data engineer building an ETL pipeline that processes financial transaction graphs to detect specific high-weight transaction chains. 

Your team uses a custom, in-house graph processing library vendored at `/app/vendor/go-graph-etl`. Recently, the pipeline has been failing because the graph loader in this library deadlocks when ingesting concurrent transaction batches. 

Your task is twofold:

1. **Fix the Deadlock:** 
   Investigate the Go package at `/app/vendor/go-graph-etl`. There is a concurrency bug in `builder.go` where adding edges between nodes concurrently causes a classic lock-ordering deadlock. Modify the package to fix the deadlock (ensure locks are acquired in a consistent, deterministic order based on Node IDs).

2. **Implement the ETL Query Process:**
   Write a Go program at `/home/user/etl_query.go` (and compile it to `/home/user/etl_query`) that imports and uses the fixed `go-graph-etl` package.
   Your program must accept a single command-line argument: the path to an input JSON file. 
   
   The input JSON is an array of edges:
   `[{"from": "node1", "to": "node2", "weight": 25}, ...]`
   
   Your program should:
   - Load the JSON and use the `go-graph-etl` package to build the graph concurrently using its `BuildGraphConcurrent(edges)` function.
   - Query the graph to find all valid paths of exactly length 3 (i.e., 4 nodes: A -> B -> C -> D).
   - Filter the paths: only include paths where the sum of the 3 edge weights is strictly greater than 100.
   - Sort the resulting paths lexicographically by the string representation of the path (e.g., "A->B->C->D").
   - Paginate the results: output ONLY the first 10 paths (or fewer if less than 10 exist).
   - Print the final result to standard output as a JSON array of strings (e.g., `["A->B->C->D", "B->X->Y->Z"]`).

Ensure your compiled executable is located at `/home/user/etl_query`. Your program must perfectly match the output of our reference implementation for any valid input graph.