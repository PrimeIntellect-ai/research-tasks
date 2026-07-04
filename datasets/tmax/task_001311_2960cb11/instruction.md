You are an AI assistant acting as a data analyst. You need to process a dataset of network transactions provided as CSV files, materialize a specific graph projection using SQLite, and expose an oracle-based scoring mechanism via a simple TCP service.

Here is the setup:
1. You have two files: `/home/user/data/nodes.csv` (columns: `node_id`, `type`) and `/home/user/data/edges.csv` (columns: `source`, `target`, `weight`).
2. There is a proprietary scoring binary located at `/app/score_oracle`. It is a stripped binary that acts as a black-box oracle. It takes two arguments: a path to a CSV file (with no header, columns: `source,target,weight`) and a `node_id`. It outputs a float risk score.

Your task:
1. **Data Processing**: Write a Bash script that loads these CSV files into an SQLite database (e.g., `/home/user/graph.db`).
2. **Graph Projection**: Using SQLite complex joins, construct a materialized table/view called `two_hop` that represents all valid 2-hop paths (A -> B -> C) where A != C. The columns must be `source` (A), `target` (C), and `weight` (the minimum of the weights of edge A->B and edge B->C). If there are multiple 2-hop paths between the same A and C, keep the one with the maximum aggregated weight.
3. **TCP Service**: Create a Bash-based TCP server that listens on `localhost:9000`. You can use `socat` or `nc`. 
   - The service must accept a single line of text containing a `node_id` (e.g., `N123\n`).
   - For the given `node_id`, query your SQLite database for all 2-hop edges where the `node_id` is the `source`.
   - Write these specific 2-hop edges to a temporary CSV file (format: `source,target,weight`, no headers).
   - Execute the oracle: `/app/score_oracle <temp_csv_path> <node_id>`.
   - Send the oracle's standard output directly back to the TCP client, followed by a newline, and close the connection.

Constraints:
- Use Bash for your scripts and server.
- The SQLite queries should be properly parameterized or safely constructed to prevent injection.
- Ensure the server runs continuously in the background and cleans up temporary files after each request.
- The service must be running before you finish the task.