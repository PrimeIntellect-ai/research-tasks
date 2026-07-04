You are a data engineer troubleshooting an ETL pipeline. An earlier SQL-based pipeline attempted to build a user co-occurrence graph but joined users on `date` instead of `session_id`, creating an implicit cross join that massively inflated the edge count and produced incorrect analytics. 

Your task is to rewrite this pipeline in Rust to correctly compute user degree centrality based on shared sessions, and export the validated results to a JSON file.

Data Location:
The raw event data is located at `/home/user/raw_events.csv`.
It has two columns: `user_id` and `session_id` (comma-separated, with a header row).

Logic Requirements:
1. Build an undirected, unweighted user-to-user graph. An edge exists between User A and User B if and only if they appear in at least one identical `session_id` together.
2. Self-loops are not permitted (a user does not have an edge to themselves).
3. Compute the "degree" of each user (the total number of unique users they share an edge with).
4. Find the top 5 users with the highest degree.
5. In case of a tie in degree, resolve it by sorting `user_id` in ascending alphabetical order (e.g., "U1" comes before "U2").

Implementation Requirements:
- You must implement the solution in Rust. Create a cargo project at `/home/user/graph_pipeline`.
- You may use standard Rust crates (like `serde`, `serde_json`, `csv`) by adding them to your `Cargo.toml`.
- After processing, output the top 5 users strictly in JSON format to `/home/user/output.json`.

Output Schema Requirements:
The JSON output must strictly follow this format:
```json
{
  "schema_version": "1.0",
  "top_users": [
    {
      "user_id": "U8",
      "degree": 6
    },
    ...
  ]
}
```

Ensure your output is written directly to `/home/user/output.json`. The verification suite will check this file's existence, its schema, and the exact values.