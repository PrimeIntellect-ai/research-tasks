You are a database administrator tasked with optimizing a sluggish data processing pipeline. 

We have a NoSQL data dump of network interactions stored in JSON Lines format at `/home/user/network_events.jsonl`. Each line represents a directed interaction between two users:
`{"source": "user_A", "target": "user_B", "timestamp": 1610000000, "type": "message"}`

A junior engineer wrote a Python script at `/home/user/compute_metrics.py` to perform graph analytics on this dataset. The script computes the In-Degree Centrality (number of incoming connections) and a simplified 2-iteration PageRank for each user. 

Unfortunately, the script performs a "cross-query aggregation" by re-reading and scanning the entire file for every single user to find their incoming edges. With the provided dataset of 10,000 events, it takes far too long to execute.

Your task:
1. Rewrite `/home/user/compute_metrics.py` so that it parses the dataset efficiently (e.g., scanning the file only once to build an in-memory graph/adjacency list).
2. Compute the exact same metrics: 
   - **In-Degree**: The absolute count of incoming edges to a user.
   - **PageRank (2 iterations)**: All nodes start with a rank of 1.0. 
     In iteration 1, each node distributes its current rank equally among its outgoing neighbors. A node's new rank is the sum of ranks it receives. (If a node has no outgoing edges, its rank is lost/sinks).
     In iteration 2, the process repeats using the ranks from iteration 1.
3. The script must output the top 5 users by In-Degree and the top 5 users by PageRank (descending order. If there is a tie, sort alphabetically by user ID).
4. Save the results to `/home/user/optimized_results.json` in exactly this format:
```json
{
  "top_in_degree": ["user_X", "user_Y", ...],
  "top_pagerank": ["user_Z", "user_W", ...]
}
```

Constraints:
- You must use standard library Python (or write a pure Python implementation). Do not rely on external libraries like `networkx` or `pandas`.
- The output file `/home/user/optimized_results.json` must exactly match the expected JSON structure.