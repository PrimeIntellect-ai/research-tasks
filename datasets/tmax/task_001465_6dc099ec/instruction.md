You are an AI assistant helping a researcher organize dataset citations.

The researcher has an SQLite database located at `/home/user/citations.db`. 
The database contains two tables:
1. `papers` (`id` INTEGER, `title` TEXT, `year` INTEGER)
2. `citations` (`source_id` INTEGER, `target_id` INTEGER, `citation_date` TEXT)

Due to a logging issue, the `citations` table contains duplicate entries for the same `(source_id, target_id)` pairs with different `citation_date`s.

Your task is to write a Python script `/home/user/export_graph.py` that projects this relational data into a materialized citation graph and exports it as JSON.

Requirements for `/home/user/export_graph.py`:
1. The script must accept two positional command-line arguments: `start_year` and `end_year` (e.g., `python3 export_graph.py 2015 2020`).
2. You must construct a parameterized SQL query (or queries) to filter papers published between `start_year` and `end_year` (inclusive).
3. Use an SQL Window Function (`ROW_NUMBER()`, `RANK()`, or `MAX() OVER()`) to deduplicate citations, keeping only the citation with the latest `citation_date` for each `(source_id, target_id)` pair.
4. The projected graph should only contain:
   - **Edges**: Deduplicated citations where BOTH the source paper and the target paper were published within the specified year range.
   - **Nodes**: Papers published within the year range that are connected to at least one edge (either as a source or a target). Isolated papers without any valid edges must be excluded.
5. The script must export the graph to `/home/user/graph.json` in the following format:
```json
{
  "nodes": [
    {"id": 1, "title": "Paper A", "year": 2015},
    ...
  ],
  "edges": [
    {"source": 2, "target": 1, "citation_date": "2016-05-05"},
    ...
  ]
}
```
6. To ensure deterministic output, sort the `nodes` list by `id` ascending, and the `edges` list by `source` ascending, then `target` ascending.

Do not use ORM libraries like SQLAlchemy; use the standard `sqlite3` library.