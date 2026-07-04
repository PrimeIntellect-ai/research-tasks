You are a Database Administrator tasked with optimizing a custom in-memory graph database engine and extracting analytical insights from a large dataset.

We have a custom graph database package vendored locally at `/app/graphdb`. Recently, it has been performing terribly on graph traversal queries. Your task is to fix the performance issue, then use the database to analyze a large graph and export the results.

Here are your instructions:
1. **Optimize the Vendored Package**: The graph database engine at `/app/graphdb` has a severe performance bottleneck in its edge retrieval logic. Inspect `/app/graphdb/store.go`. Currently, `GetEdges(nodeID string)` performs a full scan of all edges. Modify the code to implement a proper index strategy using the existing (but unused) `edgeIndex` map so that edge lookups operate in O(1) time.
2. **Implement Graph Analysis**: Write a Go program at `/home/user/analyze.go` that:
   - Imports the local `graphdb` module (you will need to initialize a go module in `/home/user` and use `replace` in `go.mod` to point to `/app/graphdb`).
   - Loads the graph dataset from `/home/user/data/edges.csv`. The CSV has headers: `source,target,weight`.
   - Uses the `graphdb` engine's `ShortestPath(start, end)` method to find the shortest path from node `"START_NODE"` to node `"END_NODE"`.
   - Computes an analytical window function over the result: calculate the **cumulative sum** of the edge weights along the shortest path.
   - Exports the final annotated path to `/home/user/result.json` as a JSON array of objects.
3. **Output Format**: `/home/user/result.json` must be strictly formatted like this:
   ```json
   [
     {"node": "START_NODE", "cumulative_weight": 0},
     {"node": "N_142", "cumulative_weight": 15},
     {"node": "N_89", "cumulative_weight": 22},
     {"node": "END_NODE", "cumulative_weight": 35}
   ]
   ```

To succeed, your compiled Go program must execute the path analysis in **under 1.0 seconds**. If you do not fix the index strategy in the vendored package, the traversal will take over 10 seconds and fail the performance metric threshold.