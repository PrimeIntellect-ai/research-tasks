You are an AI assistant helping a researcher organize and process a dataset representing a knowledge graph of academic publications. 

The researcher has provided a raw knowledge graph in JSON format located at `/home/user/knowledge_graph.json`. This file contains a list of nodes and a list of directed edges representing relationships between authors, papers, and research concepts.

The schema of `/home/user/knowledge_graph.json` is as follows:
```json
{
  "nodes": [
    {"id": "node_id", "type": "author|paper|concept", "name": "string (only for author and concept)"}
  ],
  "edges": [
    {"source": "node_id", "target": "node_id", "relation": "authored|covers"}
  ]
}
```
*   `authored` relationships always go from an `author` node to a `paper` node.
*   `covers` relationships always go from a `paper` node to a `concept` node.

Your task is to write a Python script (e.g., `/home/user/process_graph.py`) that reads this dataset and performs two analytical tasks, exporting the combined results into a strictly formatted JSON file at `/home/user/processed_results.json`.

**Task 1: Pattern Matching**
Find all unique pairs of authors who have authored *different* papers that cover the *same* concept. 
*   Represent each pair as a 2-element list containing the authors' `name`s.
*   The names within each pair must be sorted alphabetically (e.g., `["Dr. Alice", "Dr. Bob"]`).
*   The final list of pairs must be sorted lexicographically.

**Task 2: Shortest Path Computation**
Compute the shortest path length (minimum number of edges) between the author named `"Dr. Alice"` and the author named `"Dr. Bob"`. 
*   For the purpose of this traversal, treat all edges in the graph as **undirected**.
*   The path length is defined as the number of edges traversed.

**Export Format:**
Your script must output a JSON file to `/home/user/processed_results.json` with the exact following structure:
```json
{
  "pattern_matches": [
    ["AuthorName1", "AuthorName2"],
    ...
  ],
  "shortest_path_length": <integer>
}
```

Ensure your Python code handles the parsing, graph traversal, and JSON serialization using standard libraries (e.g., `json`, `collections`).