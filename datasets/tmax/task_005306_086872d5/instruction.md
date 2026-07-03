You are acting as a Database Administrator and Data Engineer. We have a fraud detection system that stores financial transactions, but our current query process is incredibly slow because it performs N+1 queries in the application layer to trace money movement.

Your task is to optimize this process by building a multi-language pipeline that chains a NoSQL aggregation pipeline with in-memory graph traversal. 

The raw data is provided in `/home/user/raw_transactions.json`. Each record represents a money transfer: `{"tx_id": "...", "from_acct": "...", "to_acct": "...", "amount": ...}`.

**Phase 1: Database Setup and Aggregation (Bash & Node.js)**
1. Install MongoDB locally (a simple local instance without auth is fine) and start the service on the default port.
2. Load the data from `/home/user/raw_transactions.json` into a MongoDB database named `fraud_db` and collection `transactions`.
3. Write a Node.js script at `/home/user/aggregate.js` that uses the official MongoDB driver to run an aggregation pipeline. The pipeline must:
   - Filter out any transactions where the `amount` is strictly less than $1000.
   - Group the remaining transactions by `from_acct` and `to_acct`.
   - Calculate the total amount transferred between each pair (as `total_volume`).
   - Output these aggregated edges into a JSON file at `/home/user/filtered_edges.json`. The file should be a JSON array of objects with keys: `from_acct`, `to_acct`, and `total_volume`. Sort this array descending by `total_volume` (pagination/sorting primitive).

**Phase 2: Graph Traversal and Summarization (Python)**
4. Write a Python script at `/home/user/shortest_path.py` that reads `/home/user/filtered_edges.json`.
5. Using a graph library (like `networkx`), build a directed graph from these edges.
6. Find the shortest path (fewest number of hops) from account `"ACCT_START"` to account `"ACCT_TARGET"`.
7. Summarize the path by calculating the sum of the `total_volume` of the edges that make up this exact shortest path.
8. Save the final result to `/home/user/solution.json` with the following exact structure:
```json
{
  "path": ["ACCT_START", "...", "ACCT_TARGET"],
  "path_volume_sum": 12345,
  "top_edge_overall": {"from_acct": "...", "to_acct": "...", "total_volume": ...}
}
```
*(Note: `top_edge_overall` should be the edge with the highest `total_volume` in the entire filtered graph, which you can easily grab since your Node.js script sorted them).*

Ensure you execute your scripts so that `/home/user/solution.json` is generated with the correct answers. You have root access via `sudo` if you need to install standard packages (like `mongodb`, `nodejs`, `npm`, `python3-pip`, `networkx`).