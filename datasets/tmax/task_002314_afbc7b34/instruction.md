You are a database reliability engineer tasked with restoring and consolidating a fragmented graph database backup. The backup system is currently spread across multiple services due to an aborted migration.

Your environment contains two running services:
1. A Python Flask service running on `127.0.0.1:5000` that serves raw graph backup chunks.
2. A Redis instance running on `127.0.0.1:6379` used as a metadata cache during the original backup process.

The Flask service has an endpoint `GET /api/chunks?page=<num>` which returns JSON arrays of fragmented graph edges and nodes. 

Your objective:
1. Write a C program located at `/home/user/graph_restore.c`.
2. The C program must interface with the Flask API to fetch all pages of the graph backup (pagination).
3. The program must reverse-engineer the underlying data model: the raw nodes have no explicit "type" labels, but their types can be inferred by their connections (e.g., nodes with only outgoing edges to specific IDs are "User" nodes, while nodes receiving those edges are "Resource" nodes).
4. Filter out any nodes that have a "status" property equal to "deleted" (and remove any dangling edges).
5. Sort the remaining nodes by their integer `id` in ascending order.
6. Export the final reconstructed graph (both inferred schema types and valid data) into a consolidated JSON-lines file at `/home/user/restored_graph.jsonl`.
   Each line should be a JSON object representing either a node `{"type": "node", "inferred_label": "User", "id": 1, ...}` or an edge `{"type": "edge", "source": 1, "target": 2}`.

Your C code must compile with `gcc /home/user/graph_restore.c -o /home/user/graph_restore -lcurl -ljansson` (you may install necessary libraries if missing).

The success of your task will be evaluated by a verification script that compares your exported `/home/user/restored_graph.jsonl` against the true original graph, calculating the accuracy of your data model inference and filtering.