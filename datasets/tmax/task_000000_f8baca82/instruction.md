You are a data analyst. You have been provided with a CSV file at `/home/user/network_data.csv` containing transaction logs for a network of users.

The CSV has the following columns:
`tx_id`, `sender`, `receiver`, `amount`, `timestamp`

Your task is to analyze this data by performing both analytical aggregations and graph analytics. 

Specifically, you must:
1. Calculate the maximum rolling 3-transaction average amount sent for each `sender`. 
   - A "rolling 3-transaction average" at any given transaction is the average of the `amount` of that transaction and up to 2 immediately preceding transactions by the SAME `sender`, ordered chronologically by `timestamp`.
   - Find the maximum value of this rolling average over the sender's history.
2. Calculate the PageRank centrality of every user (both senders and receivers) in the network.
   - Build a directed graph where edges point from `sender` to `receiver`.
   - The weight of the directed edge from X to Y should be the sum of all `amount`s sent from X to Y.
   - Use the standard PageRank algorithm (e.g., NetworkX's `pagerank` with `alpha=0.85` and default parameters, using the summed amounts as the edge `weight`).
3. Combine these metrics and output the results to `/home/user/analyzed_nodes.json`.
   - The output must be a JSON array of objects, validated to match the exact schema described below.
   - If a user never sent any transactions, their `max_rolling_3_avg` should be `0.0`.
   - Sort the JSON array alphabetically by the `node` field.
   - Round all float values to exactly 4 decimal places.

Output JSON Schema:
```json
[
  {
    "node": "string (the user's name)",
    "max_rolling_3_avg": 12.3456,
    "pagerank": 0.1234
  }
]
```

You may use any programming language or database tool (e.g., Python with `pandas`/`networkx`, SQLite window functions + Python, etc.) to accomplish this task. Ensure your final output precisely matches the requested format.