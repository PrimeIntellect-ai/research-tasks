You are a data engineer responsible for building a robust C++ ETL pipeline that transforms raw relational data into a knowledge graph, and then extracts specific subgraph patterns. 

We have a legacy SQLite database located at `/app/data.db`. It contains two tables: `nodes` and `edges`. 
Recently, we discovered that the `idx_edges_active` index on the `edges` table is corrupted. It returns stale and logically deleted rows as if they are currently active. 

Additionally, the documentation for how these relational tables map to our target graph representation has been lost in text format, but we recovered a diagram of the schema mapping and pattern requirements. It is provided as an image at `/app/schema_mapping.png`.

Your task is to:
1. Examine `/app/schema_mapping.png` to understand the cross-representation mapping from the relational tables to the graph structure, as well as the specific subgraph pattern you need to extract.
2. Write a C++ program (e.g., `pipeline.cpp`) that connects to `/app/data.db` and extracts the data. You must circumvent or fix the corrupted index issue so that you only process the truly active rows (refer to the schema mapping in the image for the definition of an active row).
3. Implement an in-memory knowledge graph representation in your C++ program and perform pattern matching to find all instances of the subgraph requested in the image.
4. Design an index strategy or query optimization within your C++ program to efficiently match the paths.
5. Export the matched subgraphs to a JSON file at `/app/matches.json`. The output schema must strictly be a JSON array of objects, where each object represents a matched path containing the node IDs in the path sequence, e.g.:
```json
[
  {"user_id": 105, "product_id": 202, "category_id": 300},
  {"user_id": 110, "product_id": 205, "category_id": 300}
]
```

You must use C++ as your primary implementation language for the ETL logic. You may install any necessary C++ libraries (e.g., `libsqlite3-dev`, `nlohmann-json3-dev`) via `apt-get`. Compile your program and run it to produce the final `/app/matches.json`.

An automated verifier will evaluate the F1 score of your extracted matches against a hidden ground truth.