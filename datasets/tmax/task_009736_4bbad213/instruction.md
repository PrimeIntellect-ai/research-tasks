You are an AI assistant helping a researcher organize and analyze a citation network dataset. 

The researcher has an RDF dataset in N-Triples format located at `/home/user/citation_graph.nt`. This dataset contains academic papers, authors, and citation links. 

The researcher needs you to write and execute a Python script (`/home/user/analyze_network.py`) that performs the following tasks:
1. **Graph Materialization**: Parse the N-Triples file using the `rdflib` Python library.
2. **Graph Projection & Traversal**: Extract all citation relationships (using the predicate `<http://example.org/ontology/cites>`). Build a directed graph using the `networkx` library and find the shortest citation path from `<http://example.org/paper/P1>` to `<http://example.org/paper/P8>`.
3. **Cross-query Aggregation**: For each paper in the resulting shortest path, use a SPARQL query via `rdflib` to determine the total number of papers written by the author of that specific paper in the path. (Assume each paper has exactly one author linked via `<http://example.org/ontology/authoredBy>`).
4. **Result Export**: Export the final data as a JSON array of objects to `/home/user/path_analysis.json`.

The exported JSON must exactly match this format:
```json
[
  {
    "paper": "http://example.org/paper/P1",
    "author_total_papers": 2
  },
  ...
]
```

Requirements:
- Ensure you install any necessary Python packages (like `rdflib` and `networkx`) locally.
- Use Python 3.
- Do not modify the original `.nt` file.