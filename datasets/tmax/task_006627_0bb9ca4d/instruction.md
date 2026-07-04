You are assisting a compliance officer in auditing a financial system for money laundering risks. Recently, an anomaly was discovered where some transaction records were missing from standard system queries, suspected to be caused by a corrupted database index. To ensure a complete audit, the compliance officer has dumped the raw transaction tables into an SQLite database and retrieved the missing archived transactions in a JSON format.

Your task is to trace the flow of funds from a suspected bad actor (Account `C-837`) to a target account (Account `C-102`) by combining these data sources and performing graph analytics.

Here are the details of the data sources:
1. **Active Database:** `/home/user/audit/active.sqlite`
   Contains a table named `transfers` with columns: `tx_id` (TEXT), `src_account` (TEXT), `dst_account` (TEXT), `amount` (REAL).
2. **Archived Documents:** `/home/user/audit/archived.json`
   Contains a JSON array of transaction objects. Each object has keys: `transaction_id`, `from_account`, `to_account`, and `transfer_value`.

**Instructions:**
1. Read and combine all transaction records from both the SQLite database and the JSON file.
2. Construct a directed graph representing the flow of funds. Each account is a node, and each transaction is a directed edge from the source account to the destination account. (If there are multiple transactions between the same two accounts, consider them as a single directed edge for the path calculation).
3. Find the shortest path (in terms of the fewest number of transaction hops) from Account `C-837` to Account `C-102`.
4. Calculate the standard **In-Degree Centrality** for all nodes in the combined graph. (In-degree centrality for a node is the fraction of nodes its incoming edges are connected to out of all possible nodes: `in_degree / (N-1)` where `N` is the total number of unique nodes in the graph).
5. Identify the "bottleneck node" along the shortest path. This is defined as the node on the shortest path (EXCLUDING the source `C-837` and target `C-102`) that has the highest In-Degree Centrality in the entire network.

**Output Requirement:**
Generate a JSON report at `/home/user/compliance_report.json` with the exact following structure:
```json
{
  "shortest_path": ["C-837", "...", "C-102"],
  "path_hops": 0,
  "bottleneck_account": "C-XXX",
  "bottleneck_centrality": 0.000
}
```
* `shortest_path`: A list of account IDs representing the path.
* `path_hops`: The number of edges in the shortest path.
* `bottleneck_account`: The account ID of the bottleneck node.
* `bottleneck_centrality`: The in-degree centrality of the bottleneck node, rounded to 4 decimal places.

Ensure the final JSON file is properly formatted. You may write and run any Python scripts needed to parse the data and compute the graph metrics.