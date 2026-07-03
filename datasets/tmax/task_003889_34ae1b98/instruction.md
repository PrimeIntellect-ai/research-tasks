You are a data engineer working on a new ETL pipeline. You have been given a SQLite database file at `/home/user/graph.db`. This database contains a graph of entities and relationships, but the exact schema and table names are undocumented. 

Your task is to:
1. Reverse engineer the schema of the database to identify the table storing the graph edges and its columns.
2. Write a Python script `/home/user/extract_patterns.py` that queries this database to find all directed "triangle" patterns where the relationship type is strictly 'friend'. A directed triangle exists if there are edges A -> B, B -> C, and C -> A (all of type 'friend').
3. Aggregate these triangles into a JSON file at `/home/user/triangles.json`. 
4. The JSON output must be a strictly formatted list of lists of integers. Each inner list should represent one triangle, containing the three node IDs sorted in ascending order. The outer list must be sorted lexicographically based on the inner lists.

Example output format for `/home/user/triangles.json`:
```json
[
  [1, 2, 3],
  [4, 5, 6]
]
```

Requirements:
- Ensure your Python script connects to the SQLite database, performs the pattern matching, aggregates the results, and dumps the JSON.
- Make sure to filter strictly for the 'friend' relationship type (there might be other types like 'follower' or 'blocks').
- Execute your script so that `/home/user/triangles.json` is generated.