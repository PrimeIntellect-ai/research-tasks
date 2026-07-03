You are a Database Reliability Engineer (DBRE) tasked with validating the replication topology from a recent NoSQL backup metadata dump. 

You have a JSON file at `/home/user/backup_metadata.json` containing an array of database nodes. Each node document has the following schema:
- `node_id` (string): Unique identifier for the database instance.
- `region` (string): The geographical region where the node is hosted.
- `replicates_from` (string or null): The `node_id` of the upstream database this node replicates from. If null, it is a root primary node.

Your objective is to write a Python script to analyze this metadata and identify cross-region replication edges within a specific hierarchical replication tree.

Specifically, you need to:
1. Parse the JSON file and materialize a directed graph representing the replication flow (from upstream to downstream).
2. Perform a recursive/hierarchical query to find the entire downstream replication tree starting from the root node: `master-eu-central-01`.
3. Within this specific downstream tree, identify all replication relationships (edges) where the upstream node and downstream node are located in *different* regions.
4. Export these specific cross-region edges into a CSV file at `/home/user/cross_region_edges.csv`.

The output CSV must have the exact following headers:
`source_id,target_id,source_region,target_region`

Sort the output rows alphabetically by `source_id`, and then by `target_id`.
Only include nodes that are part of the hierarchical tree descending from `master-eu-central-01`. Do not include cross-region edges from completely separate replication trees that might exist in the cluster backup.

Once you have written and executed the script to produce `/home/user/cross_region_edges.csv`, you are done.