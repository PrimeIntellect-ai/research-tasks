You are a data analyst tasked with building a C++ query tool to traverse a social graph stored in an SQLite database.

We have an SQLite database located at `/home/user/data/graph.db` with two tables:
- `nodes` (id INTEGER PRIMARY KEY, name TEXT, label TEXT)
- `edges` (src INTEGER, dst INTEGER, rel TEXT)

We recently discovered that the index `idx_edges_src` on the `edges` table was corrupted by a storage glitch, causing it to occasionally return stale or incorrect rows when used in query planning. 

Your objective:
1. We received an image `/app/query_pattern.png` containing a graph query pattern (in a Cypher-like syntax). Use OCR (e.g., `tesseract`) to extract the query pattern from this image.
2. Write a C++ program at `/home/user/query_tool.cpp` that implements this exact graph traversal using the SQLite C API (`sqlite3.h`).
3. Your C++ program must compile to `/home/user/query_tool`. It should take a single command-line argument: the starting node's `id` (an integer).
4. The program must print the target nodes' `name` values as specified by the query pattern, one per line, sorted alphabetically.
5. Crucially, your query MUST bypass the corrupted `idx_edges_src` index. You can do this by dropping the index before querying, or by using SQLite's `NOT INDEXED` or `INDEXED BY` clauses.

Requirements:
- Install `libsqlite3-dev` and compile with `-lsqlite3`.
- Output exactly the requested names to `stdout`, separated by newlines. Do not print any other text or debug information.