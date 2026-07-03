You are an AI assistant helping a researcher organize and analyze a corrupted datasets of academic publications. 

The researcher has an SQLite database at `/home/user/publications.db` that contains information about papers, authors, and citations. However, due to an ingestion bug, the database contains stale and duplicated rows. You need to extract the true state of the network, perform graph analysis to find the most influential papers, and export the results.

Here is the schema of the database:
- `papers`: `row_id` (INTEGER PRIMARY KEY), `paper_id` (INTEGER), `title` (TEXT), `updated_at` (INTEGER).
- `authors`: `author_id` (INTEGER PRIMARY KEY), `name` (TEXT).
- `paper_authors`: `paper_id` (INTEGER), `author_id` (INTEGER).
- `citations`: `row_id` (INTEGER PRIMARY KEY), `source_paper_id` (INTEGER), `target_paper_id` (INTEGER), `is_active` (INTEGER), `updated_at` (INTEGER).

Your objectives are:
1. **Deduplicate Records**: 
   - For `papers`, the true record for a given `paper_id` is the row with the highest `updated_at`.
   - For `citations`, the true state of a citation edge between a `source_paper_id` and `target_paper_id` is the row with the highest `updated_at` for that pair. An edge only exists in your final graph if the latest row has `is_active = 1`. If the latest row has `is_active = 0`, the citation was removed and should not be included.
   - Ignore any citations where the source or target paper is not in the set of unique `paper_id`s.

2. **Graph Analytics**:
   - Construct a directed graph where nodes are active `paper_id`s and edges are active citations (directed from `source_paper_id` to `target_paper_id`).
   - Using Python's `networkx` library, calculate the PageRank for all nodes in this directed graph. Use the default `networkx.pagerank` parameters (alpha=0.85, max_iter=100, tol=1e-06).

3. **Export Results**:
   - Find the top 3 most influential papers based on their PageRank score. If there's a tie, sort by `paper_id` ascending.
   - For each paper, find all its authors and sort the author names alphabetically.
   - Export the result as a JSON array of objects to `/home/user/top_papers.json`.

The output JSON file must exactly match this structure and have the `pagerank` rounded to 4 decimal places:
```json
[
  {
    "paper_id": 3,
    "title": "Quantum Computing Basics",
    "pagerank": 0.3521,
    "authors": ["Alice Smith", "Bob Jones"]
  },
  ...
]
```

Use Python for your scripting.