You are a data engineer building an ETL and querying pipeline for a network topology analysis tool. 

A senior engineer left a voice memo detailing the base configuration of our internal network graph. The audio file is located at `/app/network_topology.wav`. 

Your task is to:
1. Transcribe the audio file to extract the base directed edges of the network.
2. Write a Python script at `/home/user/graph_query.py` that processes document-style JSON queries against this network graph.

The script `/home/user/graph_query.py` must behave exactly as follows:
- It must initialize a directed graph containing exactly the edges described in the audio.
- It must pre-compute or dynamically compute the following metrics:
  - In-degree for all nodes.
  - PageRank for all nodes (using NetworkX's default `pagerank` implementation with `alpha=0.85`, but you must round the final answers to 4 decimal places when outputting them).
- It must read an infinite stream of JSON objects from `sys.stdin`, one per line.
- For each JSON object, it must execute the query, and print a single JSON object to `sys.stdout` containing the result, followed by a newline.

**Query Schemas and Expected Outputs:**
1. **PageRank Query**
   - Input: `{"action": "pagerank", "node": "<node_name>"}`
   - Output: `{"result": <float>}` (The PageRank value rounded to 4 decimal places. If the node does not exist, result should be `null`).
2. **Shortest Path Query**
   - Input: `{"action": "shortest_path", "source": "<node_name>", "target": "<node_name>"}`
   - Output: `{"result": ["nodeA", "nodeB", ...]}` (The list of nodes in the shortest directed path. If no path exists or nodes are invalid, result should be `null`).
3. **Top In-Degree Query**
   - Input: `{"action": "top_in_degree", "limit": <integer>}`
   - Output: `{"result": ["nodeA", "nodeB"]}` (A list of up to `<limit>` node names, sorted by in-degree descending. In case of a tie in in-degree, sort the tied nodes alphabetically ascending).

**Constraints:**
- Use standard Python 3. You may use `networkx` for graph operations.
- Ensure your script flushes standard output after every line.
- Do not print any debug information or prompts to `sys.stdout`. Only the JSON responses should be printed.
- The script must terminate gracefully when EOF is reached on `stdin`.