You are an AI assistant helping a research scientist organize their bibliographic datasets for network analysis.

The researcher has a SQLite database located at `/home/user/research.db` with the following schema:
- `authors` (id INTEGER PRIMARY KEY, name TEXT, institution TEXT)
- `papers` (id INTEGER PRIMARY KEY, title TEXT, year INTEGER, citations INTEGER)
- `paper_authors` (paper_id INTEGER, author_id INTEGER, PRIMARY KEY (paper_id, author_id))

Your task is to write a Python script `/home/user/export_graph.py` that projects this relational data into a co-authorship graph and exports it to JSON. 

Requirements for `/home/user/export_graph.py`:
1. It must accept a single command-line argument: `--min-citations` (an integer).
2. It should use parameterized SQL queries to filter out any papers that have strictly fewer than `min-citations`.
3. It must project the data into a graph format where:
   - **Nodes** are authors who have co-authored at least one paper meeting the citation threshold. 
   - **Edges** represent a co-authorship between two authors on valid papers. The "weight" of the edge should be the sum of citations of all valid papers they have co-authored together.
4. Edge deduplication: Ensure each pair of authors only has one edge, and the `source` ID is always strictly less than the `target` ID (i.e., `source_id < target_id`).
5. Export the resulting graph to a JSON file at `/home/user/coauthorship_graph.json` with the exact following structure:
```json
{
  "nodes": [
    {"id": 1, "name": "Author A"},
    {"id": 2, "name": "Author B"}
  ],
  "edges": [
    {"source": 1, "target": 2, "weight": 150}
  ]
}
```
Ensure the `nodes` are sorted by `id` ascending, and the `edges` are sorted by `source` ascending, then `target` ascending.

After creating the script, execute it with `--min-citations 50` so that the output file `/home/user/coauthorship_graph.json` is generated.