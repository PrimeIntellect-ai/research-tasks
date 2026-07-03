You are an AI assistant helping a researcher organize their dataset of academic citations.

The researcher has an SQLite database located at `/home/user/papers.db` containing two tables:
- `papers` (id INTEGER PRIMARY KEY, title TEXT, year INTEGER)
- `citations` (citer_id INTEGER, cited_id INTEGER)

A paper `A` cites paper `B` if there is a row in `citations` where `citer_id = A` and `cited_id = B`. A "citation path" from `A` to `B` means `A` cites some paper, which cites another paper, and so on, eventually citing `B`.

Your task is to write and execute a Python script at `/home/user/analyze.py` that accomplishes the following:
1. **Shortest Path**: Find the shortest citation path from paper ID `100` to paper ID `1`. Write this exact path to `/home/user/shortest_path.txt` as a single line of comma-separated paper IDs, starting with `100` and ending with `1`. (Assume there is a unique shortest path).
2. **Influence Analysis**: Find all paper IDs that transitively cite paper ID `1` (i.e., there exists a citation path from the paper to paper `1`). Write these paper IDs to `/home/user/influenced_by_1.txt`, with one ID per line, sorted in ascending numerical order.

You may use Python's built-in `sqlite3` library to execute queries. You can choose to implement the graph traversal logic in Python (e.g., using Breadth-First Search) or by using recursive SQL queries (`WITH RECURSIVE`).

Once your script is complete, run it so that the output files are generated.