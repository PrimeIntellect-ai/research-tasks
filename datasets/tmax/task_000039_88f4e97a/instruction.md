You are a data analyst optimizing a logistics network. We have raw data exported as CSVs in the directory `/home/user/data/`:
1. `nodes.csv`: Contains columns `node_id` (string), `node_type` (string).
2. `edges.csv`: Contains columns `src` (string), `dst` (string), `cost` (float).

Your goal is to process this data, perform graph analytics, construct a database, query it, and produce a validated JSON report.

Perform the following steps:

**1. Graph Analytics**
Use Python (and the `networkx` library) to treat the logistics network as an undirected graph. The edges are defined in `edges.csv` (ignore `cost` for the graph shape, treat it as unweighted). 
Calculate two metrics for every node in the network:
*   **PageRank**: Calculate the PageRank centrality. (Use the default parameters of `networkx.pagerank`).
*   **Clustering / Communities**: Detect communities using the Greedy Modularity Communities algorithm (`networkx.algorithms.community.greedy_modularity_communities`). Assign an integer `community_id` to each node based on the community it belongs to. Since the algorithm returns a list of sets (each set being a community), assign `community_id = 0` to nodes in the first set, `1` for the second set, and so on.

**2. Database & Query Optimization**
Create an SQLite database at `/home/user/logistics.db`.
Load the original node data along with your computed `pagerank` and `community_id` values into a table named `node_metrics`.
Write a SQL query that retrieves: `node_id`, `node_type`, `pagerank`, and `community_id` where `node_type` is exactly "Distribution Center".
Apply a filter to only include nodes with `pagerank > 0.01`.
Sort the results descending by `pagerank`, and then ascending by `node_id` (in case of ties).
Implement pagination to return exactly **Page 2** where the **page size is 5** (meaning, skip the first 5 records and return the next 5).

Output the `EXPLAIN QUERY PLAN` of this exact query to `/home/user/query_plan.txt`.

**3. Output & Schema Validation**
Execute your paginated query and export the results to `/home/user/result.json` as a JSON array of objects. 
The JSON must strictly conform to this JSON schema, which is already saved at `/home/user/schema.json`:
```json
{
  "type": "array",
  "items": {
    "type": "object",
    "properties": {
      "node_id": { "type": "string" },
      "node_type": { "type": "string" },
      "pagerank": { "type": "number" },
      "community_id": { "type": "integer" }
    },
    "required": ["node_id", "node_type", "pagerank", "community_id"],
    "additionalProperties": false
  }
}
```
Finally, write a brief Python script at `/home/user/validate.py` that uses the `jsonschema` library to validate `/home/user/result.json` against `/home/user/schema.json`. Ensure that running `python3 /home/user/validate.py` exits successfully with code 0 if the data is valid.