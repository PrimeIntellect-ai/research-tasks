You are a database reliability engineer tasked with creating a localized backup tool for a legacy graph database.

Our application stores graph data in an SQLite database located at `/home/user/graph.db`. Unfortunately, the original documentation is lost, so you will need to inspect the database to understand its schema (it contains tables for nodes and directed edges, but the exact table and column names are unknown).

Your task is to write a Bash script `/home/user/backup_neighborhood.sh` that takes a single integer argument (a node ID) and exports the 1-hop neighborhood of that node into a nicely formatted JSON file. 

The 1-hop neighborhood includes:
- The center node itself.
- All nodes that have an edge to or from the center node.
- All edges where the center node is either the source or the target.

The script must:
1. Query the SQLite database.
2. Chain the results into `jq` to construct the JSON.
3. Save the resulting JSON to `/home/user/backup_<node_id>.json`.

The output JSON must strictly match this structure:
```json
{
  "center_node": <node_id_as_integer>,
  "nodes": [
    {
      "id": <node_id_as_integer>,
      "data": "<exact_string_from_the_properties/data_column>"
    }
  ],
  "edges": [
    {
      "source": <source_node_id>,
      "target": <target_node_id>,
      "type": "<edge_type_string>"
    }
  ]
}
```

Requirements for the output:
- The `nodes` array must be sorted by `id` in ascending order.
- The `edges` array must be sorted by `source` ascending, then `target` ascending.
- The output file must be valid, pretty-printed JSON.

Please create the bash script and ensure it has executable permissions. You may use standard tools like `sqlite3` and `jq`. Ensure your script dynamically handles any node ID passed to it.