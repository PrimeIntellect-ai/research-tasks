I am a researcher organizing a disorganized scientific dataset containing papers, authors, and citation networks. My previous concurrent data ingestion pipeline failed due to transaction deadlocks, leaving me with a raw SQLite database file at `/home/user/research_data.db` without any documentation on its schema. 

I need you to write a Python script at `/home/user/analyze_graph.py` to analyze this dataset and extract a specific chain of citations. 

Your tasks are to:
1. **Reverse Engineer the Data Model**: Inspect `/home/user/research_data.db` to understand how papers, authors, and citations are stored.
2. **Graph Traversal**: Compute the shortest directed citation path (source paper citing target paper, chaining forward) from the paper titled "Quantum Origins" to the paper titled "Macroscopic Superposition". 
3. **Parameterized Queries**: For every paper in this shortest path (including the start and end papers), use parameterized SQL queries to securely retrieve the paper's title, publication year, and a list of all its authors.
4. **Schema Validation & Output**: Save the results of your pipeline to `/home/user/path_results.json`. The JSON file must strictly be an array of objects representing the path in chronological order of the traversal (from "Quantum Origins" to "Macroscopic Superposition"). 

The output JSON must strictly adhere to this schema structure:
```json
[
  {
    "title": "String",
    "year": "Integer",
    "authors": ["String", "String"] 
  }
]
```
Note: Ensure the authors array is sorted alphabetically for each paper.

You may install any required Python packages (e.g., `networkx` for graph operations, though standard BFS is also fine) into the local environment using `pip`.