You are a data analyst working with a dataset of network interactions. Your goal is to process a CSV file of edge connections, project it into a structured graph format, and export it as a nested JSON document (similar to a NoSQL aggregation pipeline output).

You have been provided with a CSV file at `/home/user/analytics/network.csv`. The CSV has no header and contains three columns:
1. `source` (string)
2. `target` (string)
3. `interaction_count` (integer)

Write a Go program located at `/home/user/analytics/build_graph.go` that does the following:
1. Reads the `network.csv` file.
2. Loads the data into a local SQLite database file named `/home/user/analytics/graph.db` in a table named `edges`.
3. Accepts an integer threshold as a command-line argument (e.g., `go run build_graph.go 10`).
4. Uses parameterized SQL queries to find all `source` nodes whose *total* `interaction_count` (summed across all their targets) is strictly greater than the provided threshold.
5. For these qualifying source nodes, retrieves their individual target connections and constructs a nested graph projection.
6. Exports the result to a JSON file at `/home/user/analytics/output.json`.

The exported JSON must be a formatted array of objects (using standard 2-space indentation), with the following exact structure:
```json
[
  {
    "source_node": "A",
    "total_interactions": 15,
    "connections": [
      {
        "target_node": "B",
        "weight": 10
      },
      {
        "target_node": "C",
        "weight": 5
      }
    ]
  }
]
```

**Sorting Requirements:**
- The outer JSON array must be sorted alphabetically by `source_node`.
- The inner `connections` array for each source must be sorted alphabetically by `target_node`.

**Execution:**
Once your Go program is written, execute it with a threshold of `10`:
`cd /home/user/analytics && go run build_graph.go 10`

Ensure the final `output.json` is generated correctly.