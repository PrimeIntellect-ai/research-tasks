I am a database administrator working on a logistics application. We have a SQLite database located at `/home/user/logistics.db` that stores our cities and the connections between them. 

I wrote a Python script at `/home/user/route_solver.py` to extract these routes, find the shortest path between 'Alpha' and 'Omega', and export the result. However, the script is broken. The SQL query inside it is doing an implicit cross join, causing it to return a massive number of incorrect, duplicated rows with mismatched cities and distances. Furthermore, I haven't finished implementing the graph traversal and export logic.

Your task is to fix the script to fulfill these requirements:
1. **Fix the SQL Query**: Modify the SQL query in `/home/user/route_solver.py` to correctly map `locations` to `connections`. The `connections` table has `loc1_id` (source) and `loc2_id` (destination). You must use explicit `JOIN`s to get the correct `source_name`, `dest_name`, and `distance_km`. Only include connections where `active = 1`. Connections are one-way (directed) from source to destination.
2. **Implement Graph Traversal**: Using the results from the corrected query, build a graph and compute the shortest path from the city named 'Alpha' to the city named 'Omega'.
3. **Export the Results**: Save the final computed shortest path and its total distance to a JSON file at `/home/user/shortest_path.json`.

The exported JSON must perfectly match this structure:
```json
{
  "path": ["Alpha", "SomeCity", "Omega"],
  "total_distance": 123
}
```

Database Schema:
- `locations` table: `id` (INTEGER PRIMARY KEY), `name` (TEXT)
- `connections` table: `id` (INTEGER PRIMARY KEY), `loc1_id` (INTEGER), `loc2_id` (INTEGER), `distance_km` (INTEGER), `active` (INTEGER)

Please fix `/home/user/route_solver.py` and run it so that `/home/user/shortest_path.json` is generated correctly.