You are a database administrator tasked with fixing a performance and accuracy issue in a graph analytics pipeline.

You have a SQLite database at `/home/user/graph.db` with two tables representing a knowledge graph:
- `nodes` (id INTEGER PRIMARY KEY, type TEXT)
- `edges` (src INTEGER, dst INTEGER)

There is a Python script at `/home/user/analyze.py` that is supposed to find the top node for each `type` based on its "extended degree". The extended degree is defined as the number of unique nodes that can be reached via exactly a 2-hop path (i.e., `source -> intermediary -> destination`). 

Currently, the SQL query inside `/home/user/analyze.py` produces wildly incorrect results and is very slow. This is because the query contains an implicit cross join in its Common Table Expression (CTE), joining on the wrong condition which multiplies the rows incorrectly.

Your tasks:
1. Debug and fix the SQL query in `/home/user/analyze.py`. 
    - Fix the join condition so that it correctly traverses the edges (`n.id = e1.src`, `e1.dst = e2.src`, and `e2.dst = n2.id`).
    - The query should calculate the extended degree (count of distinct destination nodes for exactly 2 hops) for each node.
    - Use window functions to rank the nodes within each `type` partition by their extended degree in descending order. In case of a tie, rank by `id` in ascending order.
2. Modify `/home/user/analyze.py` to execute the fixed query, filter for nodes with rank = 1 for each type, and export the results to `/home/user/top_nodes.json`.

The output `/home/user/top_nodes.json` must be a JSON array of objects, containing exactly the top node for each type, formatted like this:
```json
[
  {
    "type": "A",
    "id": 12,
    "ext_degree": 5
  },
  {
    "type": "B",
    "id": 4,
    "ext_degree": 3
  }
]
```

Ensure the keys are exactly `type`, `id`, and `ext_degree`.