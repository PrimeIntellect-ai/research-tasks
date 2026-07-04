You are an AI assistant helping a researcher clean and analyze a dataset of academic citations. 

The researcher has an SQLite database located at `/home/user/citation_graph.db` with the following schema:
- Table `papers`: `id` (INTEGER), `title` (TEXT)
- Table `citations`: `source_id` (INTEGER), `target_id` (INTEGER)

Due to a historical bug in the researcher's scraping script and a corrupted database index that wasn't properly dropping stale rows, the `citations` table contains messy data:
1. There are duplicate citation edges (the exact same `source_id` and `target_id` pair appears multiple times).
2. There are self-citations (where `source_id` equals `target_id`).

Your task is to build a Python-based data pipeline that queries this database, constructs a clean graph in memory, and performs graph analytics. 

You must write a Python script (or use the terminal) to do the following:
1. Extract the citation data, strictly ignoring duplicate edges and ignoring any self-citations.
2. **Graph Analytics:** Calculate the In-Degree (number of incoming citations) for every paper in the clean graph. Identify the `id` of the paper with the highest In-Degree.
3. **Graph Traversal:** Compute the shortest directed path (fewest number of edges) from paper ID `10` to paper ID `42`. 
4. **Output Schema Validation:** Write your final answers to a JSON file at `/home/user/research_results.json` that strictly conforms to the following format:
```json
{
  "most_cited_paper_id": 0,
  "highest_in_degree": 0,
  "shortest_path_10_to_42": [10, ..., 42]
}
```
Replace the `0`s and the array with your computed integer results. If there is a tie for the most cited paper, return the one with the lowest `id`.

Ensure your Python code doesn't rely on heavy external libraries like Neo4j or NetworkX unless you install them yourself; standard library tools like `sqlite3`, `json`, and basic BFS queue implementations (using `collections.deque`) are highly recommended.