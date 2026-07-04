You are an AI assistant helping a network science researcher organize and analyze a dataset of academic collaborations. 

The researcher has dumped their bibliographic data into a SQLite database located at `/home/user/network.db`. However, they lost the schema documentation. You need to inspect the database, understand its schema, and extract specific insights combining graph traversal and aggregation.

Your objectives are:
1. **Schema Analysis**: Analyze `/home/user/network.db` to understand how authors, papers, and authorship relations are stored. Two authors are considered "connected" if they have co-authored at least one paper together.
2. **Graph Traversal**: Find the shortest collaboration path between the author named `"Alice Smith"` and the author named `"Bob Jones"`. 
3. **Cross-Query Aggregation**: Calculate the total number of *unique* papers authored or co-authored by *any* of the authors included in that shortest path.
4. **Query Plan Extraction**: Save the SQLite execution plan (`EXPLAIN QUERY PLAN`) of the SQL query you use to find the co-authorship connections into `/home/user/query_plan.txt`.
5. **Result Export**: Output your final findings in a strictly formatted JSON file at `/home/user/summary.json`. The JSON must have exactly this structure:
```json
{
  "shortest_path": ["Alice Smith", "Intermediary 1", "Intermediary 2", "Bob Jones"],
  "total_unique_papers": 42
}
```

Notes:
- You may write a script in any language (Python, Node.js, bash + sqlite3, etc.) to perform the graph traversal, queries, and aggregations.
- `shortest_path` should be an ordered list of author names starting with "Alice Smith" and ending with "Bob Jones". 
- There is exactly one unique shortest path between them in the dataset.
- Make sure `/home/user/summary.json` and `/home/user/query_plan.txt` are written successfully before you finish.