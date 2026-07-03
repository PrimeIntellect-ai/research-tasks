You are a data analyst working with supply chain logistics. You have been provided with a CSV file at `/home/user/routes.csv` containing network routes. The file has the following header: `source,destination,cost,capacity,type`.

You need to write a Go program `/home/user/analyze.go` that reads this CSV file and performs two specific analytical queries:

1. **Shortest Path Query**: 
   Find the minimum cost path from `"FactoryA"` to `"StoreZ"`.
   *Constraint*: You must ONLY traverse edges (routes) that have a `capacity >= 50`. 
   Compute the path sequence and the total cost.

2. **Aggregation Pipeline Query**:
   Implement an in-memory aggregation pipeline that:
   - Filters only routes where `type == "express"`
   - Groups the filtered routes by `source`
   - Calculates the `avg_cost` (average cost of outbound express routes from that source) and `total_capacity` (sum of capacities of outbound express routes from that source)
   - Sorts the grouped results by `avg_cost` in descending order. If there is a tie in `avg_cost`, sort by `source` alphabetically.
   - Limits the result to the top 3 sources.

Your Go program must write the results to `/home/user/results.json` exactly matching this JSON structure:

```json
{
  "shortest_path": {
    "path": ["FactoryA", "...", "StoreZ"],
    "total_cost": 120
  },
  "top_express_sources": [
    {
      "source": "SourceName",
      "avg_cost": 45.5,
      "total_capacity": 500
    }
  ]
}
```

Requirements:
- Ensure your `analyze.go` program is fully self-contained (using standard library only).
- Do not assume the CSV data fits a specific size; use appropriate data structures for graph traversal and grouping.
- Ensure the output JSON file is perfectly formatted.
- You must compile and run the Go program to generate the `/home/user/results.json` file.