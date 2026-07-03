You are a data analyst working with financial transaction networks. We need to process a dataset of transactions, model it as a directed graph, compute centrality metrics, and simulate a NoSQL aggregation pipeline to cluster the entities based on their net flow.

Your task is to write a Go program at `/home/user/graph_pipeline.go` that does the following:

1. **Read Data**: Read a CSV file located at `/home/user/edges.csv`. The CSV has a header `source,target,weight` where `source` and `target` are string IDs (e.g., "U1", "U2") and `weight` is an integer representing transaction volume.
2. **Graph Analytics (Centrality)**: Map the CSV into a graph representation in memory. For each node, calculate:
   - `InWeight`: Sum of weights of all incoming edges.
   - `OutWeight`: Sum of weights of all outgoing edges.
   - `Activity`: Total activity of the node (`InWeight + OutWeight`).
3. **Cross-representation Pipeline**: Simulate a NoSQL aggregation pipeline that assigns each node to a cluster and groups them:
   - Assign a cluster role based on net flow (`InWeight - OutWeight`):
     - `"net_sink"` if InWeight > OutWeight
     - `"net_source"` if OutWeight > InWeight
     - `"balanced"` if InWeight == OutWeight
   - Group the nodes by their cluster role.
4. **Aggregation Output**: Output a single JSON file to `/home/user/aggregated_roles.json` with the following strict structure:
   ```json
   {
     "net_sink": {
       "nodes": ["U2", "U4"], 
       "total_activity": 1500
     },
     "net_source": {
       "nodes": ["U1", "U3"],
       "total_activity": 1200
     },
     "balanced": {
       "nodes": ["U5"],
       "total_activity": 300
     }
   }
   ```
   **Rules for JSON**:
   - The top-level keys must exactly match the cluster roles that exist in the data (if a cluster has no nodes, you may either omit it or include it with empty/0 values, but the test will check existing keys).
   - The `nodes` array for each cluster MUST be sorted lexicographically (ascending).
   - `total_activity` is the sum of the `Activity` metric for all nodes in that cluster.

You must write and run the Go script to produce the output file. You have standard Go packages available. No external dependencies are required. Do not modify the input CSV.