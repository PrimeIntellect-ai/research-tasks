You are an AI assistant helping a data researcher organize and analyze citation datasets. 

The researcher has a set of citation records stored as JSON documents, but needs them mapped into a relational database for querying, and then loaded into an in-memory graph to perform graph analytics. Finally, the results must be exported into a strictly validated JSON format. 

Your task is to write and execute a C++ program that handles this entire pipeline.

**Prerequisites & Setup:**
The system is running Ubuntu. You will need to install any necessary C++ libraries (e.g., `libsqlite3-dev`, `nlohmann-json3-dev`, `build-essential`, `cmake`).
The dataset is provided at `/home/user/dataset/citations.jsonl`. Each line is a JSON object with the following schema:
`{"paper_id": "string", "cites": ["string", "string", ...]}`

*Note: You must create this file first with the following mock dataset to test your code before final execution:*
```jsonl
{"paper_id": "P1", "cites": ["P2", "P3"]}
{"paper_id": "P2", "cites": ["P3"]}
{"paper_id": "P3", "cites": ["P1", "P4"]}
{"paper_id": "P4", "cites": []}
{"paper_id": "P5", "cites": ["P1", "P4"]}
```

**Requirements for the C++ Program:**
Write a C++ program (e.g., in `/home/user/workspace/analyze.cpp`) that performs the following steps:

1. **Cross-Representation Mapping (Document to Relational):**
   - Parse the `/home/user/dataset/citations.jsonl` file.
   - Create an SQLite database at `/home/user/workspace/graph.db`.
   - Create two tables: 
     - `Papers (id TEXT PRIMARY KEY)`
     - `Citations (source TEXT, target TEXT)`
   - Insert the parsed JSON data into these tables. (Ensure you handle SQLite transactions efficiently).

2. **Graph Analytics (Centrality):**
   - Query the SQLite database to build a directed graph in memory (using standard C++ containers).
   - Calculate the **Degree Centrality** for every paper in the network. For this directed graph, Degree Centrality is defined as the sum of In-Degree + Out-Degree.
   - *Note:* Make sure to include all papers, even those that have a degree of 0 (though our dataset ensures most have connections) or papers that are cited but don't appear as a primary `paper_id` in the JSON (e.g., if P6 is cited but has no entry, it still exists in the network with an in-degree of 1 and out-degree of 0).

3. **Output Schema Validation:**
   - Export the centrality results to `/home/user/workspace/centrality_results.json`.
   - The output must strictly match this exact JSON format:
     ```json
     {
       "metrics": [
         {"node": "P1", "degree_centrality": 4},
         {"node": "P2", "degree_centrality": 2}
       ]
     }
     ```
   - The array must be sorted in descending order of `degree_centrality`. If there is a tie, sort alphabetically by `node` ID.

Build and run your C++ program so that `/home/user/workspace/graph.db` and `/home/user/workspace/centrality_results.json` are successfully generated and populated.