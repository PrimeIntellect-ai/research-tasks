You are helping a researcher organize and analyze a citation network dataset. 

A SQLite database containing the citation network is located at `/home/user/citations.db`. It has two tables:
- `papers` (columns: `id` TEXT, `title` TEXT)
- `citations` (columns: `source_id` TEXT, `target_id` TEXT) representing a directed citation from `source_id` to `target_id`.

Your task involves several steps:
1. **Index Strategy:** The database currently has no indexes, making queries slow. Create the optimal indexes on the `citations` table to speed up graph traversal queries (finding outgoing and incoming citations).
2. **Graph Traversal:** Write a Python script to compute the shortest citation path from the paper with ID `P1` to the paper with ID `P5`. You may use a standard breadth-first search (BFS) algorithm in Python by querying the database, or use SQLite's recursive CTEs.
3. **Export and Format:** Export the result to a JSON file located at `/home/user/shortest_path.json`. The JSON must precisely match this format:
```json
{
  "path_length": <integer_number_of_edges>,
  "path": [
    {"id": "<paper_id>", "title": "<paper_title>"},
    ...
  ]
}
```
4. **Validation:** A JSON schema is provided at `/home/user/schema.json`. Your final JSON output must strictly validate against this schema.

Please execute the necessary database modifications and create/run the Python script to produce `/home/user/shortest_path.json`.