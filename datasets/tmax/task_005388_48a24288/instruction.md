You are helping a researcher organize and analyze a massive citation dataset stored in an SQLite database. You need to extract a specific citation subgraph, perform analytical aggregations, and write a C++ filter to sanitize the output against adversarial data.

**Step 1: Extract Setup Information from Image**
There is a scanned note from the principal investigator located at `/app/root_node.png`. You must use OCR (e.g., `tesseract`) to read it. It contains the `START_NODE` (a paper ID) and `MAX_DEPTH` for a graph traversal.

**Step 2: Database Query & Graph Materialization**
The database is located at `/app/research.db`. 
It has two tables:
- `papers(id INTEGER PRIMARY KEY, title TEXT, year INTEGER, citations INTEGER, is_deleted INTEGER)`
- `edges(source_id INTEGER, target_id INTEGER, is_deleted INTEGER)`

*Warning:* The database recently suffered a crash. The index `idx_edges_source` on the `edges` table is corrupted and returns "stale" rows where `is_deleted=1`. You must write your query to bypass or explicitly filter out deleted rows, ensuring no `is_deleted=1` records are included in your results.

Write an SQLite script (using CTEs) that:
1. Projects a graph starting from the `START_NODE` (from Step 1) up to `MAX_DEPTH`.
2. For all unique papers discovered in this subgraph, use a window function to calculate their `rank` based on their `citations` count, partitioned by `year` (order by citations DESC).
3. Paginate the final result: select only the top 50 rows, ordered by `year` ASC, then `rank` ASC.
Save your SQL query to `/home/user/query.sql` and the CSV output to `/home/user/projected_graph.csv`.

**Step 3: C++ Adversarial Path Filter**
The researcher is dealing with bot-generated cyclic citation rings. You must write a C++ program that acts as a filter.
- The program should read lines from standard input.
- Each line represents a citation path as a comma-separated list of paper IDs (e.g., `102,405,102,994`).
- **Clean data:** Paths where all paper IDs in the sequence are strictly unique (acyclic).
- **Evil data:** Paths that contain at least one duplicate paper ID (a cycle).
- The program must write ONLY the clean lines to standard output, unmodified.
- Compile your program to `/home/user/path_filter`.

Ensure your C++ program is highly efficient, as it will be tested against a massive corpus of clean and evil paths to verify it correctly rejects 100% of cyclic paths and preserves 100% of acyclic paths.