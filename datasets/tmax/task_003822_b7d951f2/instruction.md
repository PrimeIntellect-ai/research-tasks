You are a data analyst working with an older network routing system. The system's backend is an SQLite database located at `/home/user/routing.db`. We recently discovered that a corrupted index is causing raw queries to occasionally return stale, inactive routing paths alongside active ones. 

The database has a single table named `network_links` with the following schema:
`CREATE TABLE network_links (source TEXT, target TEXT, latency INTEGER, is_active INTEGER);`

Your task is to:
1. Extract the active network topology (where `is_active = 1`) from the SQLite database. Be sure to use `DISTINCT` to avoid any duplicated active rows caused by the index corruption.
2. Write and execute a Python script (`/home/user/find_path.py`) that reads this extracted data and computes the shortest path (lowest total latency) from the node named `START` to the node named `END`. The graph is directed.
3. Export the shortest path result to a CSV file at `/home/user/shortest_path.csv`.

The output file `/home/user/shortest_path.csv` must contain exactly two columns: `node` and `cumulative_latency`, representing the sequence of nodes visited and the total latency from `START` up to that node. Include a header row.

Example output format:
```csv
node,cumulative_latency
START,0
NODE_A,5
NODE_B,12
END,15
```