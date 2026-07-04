You are a database administrator tasked with optimizing and securing a new network topology query system. The system relies on a locally stored SQLite database, but there are several issues you need to resolve, spanning data integrity, complex querying, and security.

Your task has four main stages:

**Stage 1: Parameter Extraction**
A former engineer left a screenshot with the critical parameters needed to query the topology. The image is located at `/app/schema_clue.png`. You must use optical character recognition (OCR) tools (like `tesseract`, which is preinstalled) to read the text in this image. You are looking for two specific values:
1. The `ROOT_NODE` ID.
2. The `EDGE_TYPE` string.

**Stage 2: Database Data Integrity and Reverse Engineering**
The SQLite database is located at `/home/user/network_topology.db`. You must reverse engineer its schema. It contains nodes and edges representing network connections. 
There is a known issue: an old, corrupted index on the edges table is causing queries to return stale, duplicate rows with incorrect high-cost values. You must identify this index, drop it, and optionally create a new, correct index to ensure that subsequent queries only read the valid data.

**Stage 3: Shortest Path Computation**
Using the `ROOT_NODE` and `EDGE_TYPE` recovered in Stage 1, write a Python script at `/home/user/compute_paths.py`. This script must connect to `/home/user/network_topology.db` and execute a recursive SQL query (CTE) to compute the shortest path (the path with the minimum sum of edge costs) from the `ROOT_NODE` to all other reachable nodes, considering ONLY edges that match the recovered `EDGE_TYPE`.

The script should output a CSV file to `/home/user/shortest_paths.csv` with exactly three columns, including a header:
`target_node_id,total_cost,path_string`
* `target_node_id`: The ID of the destination node.
* `total_cost`: The numeric sum of the edge costs along the shortest path.
* `path_string`: A string representing the node IDs in the path separated by arrows, e.g., `1042->305->992`.

**Stage 4: Adversarial Query Sanitization**
The engineering team wants to expose a read-only query endpoint but is worried about SQL injection and malicious modifications. You must build a Python CLI tool at `/home/user/query_sanitizer.py`.
* It must accept exactly one argument: the absolute path to a text file containing a SQL query.
* Example invocation: `python3 /home/user/query_sanitizer.py /path/to/query.sql`
* The script must read the query from the file.
* If the query is a safe, read-only `SELECT` query, it must exit with status code `0`.
* If the query contains malicious patterns (e.g., attempts to `DROP`, `DELETE`, `UPDATE`, `INSERT`, `ALTER`, or uses SQL comment injection like `--` or `/*`), it must exit with status code `1`.
* Your script will be tested against two hidden corpora of queries. It must perfectly accept all clean queries and reject all evil queries.

Ensure all scripts are executable and well-documented. You may use standard Linux terminal commands and write code in multiple languages (bash, Python) as needed.