You are a data analyst working with supply chain network data. You have been provided with three CSV files representing a knowledge graph of logistics nodes, their connections, and a set of routing queries.

Your task is to write a Go program `/home/user/analyze.go` that processes these files, validates the schema integrity, computes shortest paths based on specific knowledge graph patterns, and outputs an aggregated summary.

Here are the specific requirements:

1. **Input Files:**
   - `/home/user/nodes.csv`: Contains two columns `node_id` and `node_type`.
   - `/home/user/edges.csv`: Contains four columns `src`, `dst`, `cost` (float), and `rel` (string).
   - `/home/user/queries.csv`: Contains two columns `start` and `end`.
   *(Assume all CSVs have headers. You must parse them accordingly).*

2. **Schema Validation:**
   - Your program must first validate that every `src` and `dst` referenced in `edges.csv` actually exists in `nodes.csv`.
   - Any missing node IDs discovered during this validation must be written to `/home/user/validation_errors.log`, with exactly one missing `node_id` per line, sorted alphabetically.

3. **Knowledge Graph Pattern & Traversal:**
   - Build a directed graph from `edges.csv`.
   - **Pattern Matching Rule:** You must ONLY include edges where the `rel` (relationship) is either `CONNECTED_TO` or `DEPENDS_ON`. Edges with any other relationship (like `INCOMPATIBLE_WITH`) must be completely ignored for routing.
   - For each row in `queries.csv`, calculate the shortest path cost from `start` to `end` using Dijkstra's algorithm.

4. **Cross-Query Aggregation:**
   - Aggregate the results of your path finding into a single JSON output file at `/home/user/summary.json`.
   - The JSON must match this exact schema:
     ```json
     {
       "total_queries": <integer, total number of queries in queries.csv>,
       "successful_paths": <integer, number of queries where a valid path was found>,
       "total_cost": <float, sum of costs of all successful shortest paths>,
       "average_cost": <float, total_cost divided by successful_paths (0 if none)>
     }
     ```

Write the Go code, compile/run it, and ensure that both `/home/user/validation_errors.log` and `/home/user/summary.json` are generated successfully. Do not use any third-party Go libraries; stick strictly to the standard library.