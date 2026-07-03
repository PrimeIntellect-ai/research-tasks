You are a Database Reliability Engineer (DBRE) tasked with validating our NoSQL backup infrastructure. We model our database replication topology as a directed knowledge graph. 

You have a Rust tool located in `/home/user/backup_graph` that processes a NoSQL backup manifest (`/home/user/backup_manifest.json`). The tool is supposed to calculate the total storage footprint of a replication chain by performing a recursive hierarchical query (graph traversal) starting from a specific root node (`db_primary`).

However, the current Rust code contains a logical error in the query pipeline. When matching edges to nodes to resolve the hierarchy, it forgets to enforce a strict join condition. This results in an implicit cross-join behavior, causing the traversal to multiply sizes incorrectly and return a massively inflated storage footprint.

Your task:
1. Navigate to `/home/user/backup_graph`.
2. Inspect and fix the Rust code in `src/main.rs`. Identify the implicit cross-join bug in the graph pattern matching logic and correct it so that it properly traverses the explicit parent-child replication edges.
3. Build and run the project.
4. The program will output the total size of the `db_primary` replication chain to the standard output.
5. Save exactly this correct numeric total to a file at `/home/user/report.txt`.

Ensure your fix actually traverses the tree structure correctly (matching edge targets to node IDs) rather than hardcoding the result.