You are an AI assistant helping a data researcher organize and query a hierarchical dataset.

The researcher has provided:
1. A SQLite database `/app/knowledge_graph.db` containing a hierarchical knowledge graph. The database has a table `nodes(id INTEGER PRIMARY KEY, name TEXT, parent_id INTEGER, value REAL)`. `parent_id` is a self-referencing foreign key creating a hierarchy. 
2. An image `/app/query_criteria.png` which contains a screenshot of the researcher's notes. 
3. A JSON schema file `/app/output_schema.json`.

Your task:
1. Read the image `/app/query_criteria.png` to extract the list of "Target Root Nodes" and the "Minimum Aggregate Value". You can use `tesseract` or any other tool to perform OCR on the image.
2. Write a Python script `/home/user/aggregate.py` that connects to the SQLite database.
3. For each of the Target Root Nodes extracted from the image, use a recursive CTE (Common Table Expression) to find all of its descendant nodes in the hierarchy (including the root node itself).
4. Compute the total sum of the `value` column for each target node's entire subtree.
5. Filter out any target nodes where the total subtree sum is strictly less than the "Minimum Aggregate Value" extracted from the image.
6. The script must output the surviving target nodes and their aggregated values as a JSON list of objects, e.g., `[{"root_name": "...", "total_value": ...}]`.
7. Before writing to disk, your script must validate the constructed JSON data against the schema in `/app/output_schema.json` using the Python `jsonschema` library.
8. Save the validated JSON output to `/home/user/results.json`.

Ensure your Python script runs cleanly and generates the correct `/home/user/results.json`. The precision of your floating-point sums should be to at least 4 decimal places.