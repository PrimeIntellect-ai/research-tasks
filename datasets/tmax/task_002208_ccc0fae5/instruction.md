You are a data engineer tasked with building an ETL pipeline to analyze transaction graphs using Bash and standard CLI utilities (`awk`, `jq`, `sort`, etc.). 

You have been provided with a raw CSV file at `/home/user/transactions.csv` containing transaction logs. The file has a header and the following columns: `sender`, `receiver`, `amount`, `timestamp`.

Your objective is to write a Bash script `/home/user/pipeline.sh` that performs the following steps:
1. **Filtering**: Ignore the CSV header. Filter out any transactions where the `amount` is strictly less than or equal to `10`.
2. **Graph Projection**: Aggregate the filtered transactions into a directed graph. The nodes are the account IDs. An edge exists from `sender` to `receiver` with a weight equal to the sum of all transaction amounts from that `sender` to that `receiver`.
3. **Graph Analytics (Centrality)**: For each node in the graph (whether they appear as a sender, receiver, or both), compute the following degree centrality metrics based on the projected graph:
   - `out_deg`: Number of unique receivers the node sends to.
   - `in_deg`: Number of unique senders the node receives from.
   - `total_out`: The total sum of weights of all outgoing edges.
   - `total_in`: The total sum of weights of all incoming edges.
   *(Note: If a node has no incoming edges, `in_deg` and `total_in` should be 0. Same for outgoing)*
4. **Sorting and Pagination**: Sort the nodes primarily by `total_out` in descending order, and secondarily by node ID alphabetically in ascending order. Retrieve the top 3 nodes.
5. **Output Schema Validation**: Output the top 3 nodes as a pretty-printed JSON array of objects to `/home/user/top_nodes.json`. Each object must strictly match the following schema keys and types:
   - `"node"` (string)
   - `"out_deg"` (integer)
   - `"in_deg"` (integer)
   - `"total_out"` (integer)
   - `"total_in"` (integer)

Ensure your script `/home/user/pipeline.sh` is executable and generates `/home/user/top_nodes.json` when run. Do not use external scripting languages like Python or Perl; stick to standard Unix tools (Bash, awk, jq, etc.).