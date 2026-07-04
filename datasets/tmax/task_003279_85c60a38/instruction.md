You are assisting a data researcher who has mapped out the complex lineage of their datasets and models, but unfortunately, only has this mapping as an image of a text document.

Your task is to extract this dependency graph and expose it as a running API service so the researcher's automated tools can query the dataset lineage.

1. Locate the image at `/app/dataset_lineage.png`. It contains lines of text indicating data flow. Each line is formatted as `SOURCE -> DESTINATION`, meaning the `DESTINATION` dataset is derived from the `SOURCE` dataset.
2. Use OCR (e.g., `tesseract`, which is installed) to extract the text from the image. Clean up any obvious OCR errors (assume node names only consist of uppercase letters).
3. Build an HTTP server listening on `127.0.0.1:8000` that serves this graph data. You may use any language (e.g., Python, Node) and install any packages you need. 
4. Implement the following two API endpoints:
   - `GET /upstream?dataset=<NODE_NAME>`: Returns a JSON object `{"upstream": [...]}` containing a deduplicated, lexicographically sorted array of all ancestral nodes (the datasets that this node depends on, directly or transitively). If the node has no upstream dependencies or doesn't exist, return an empty array.
   - `GET /downstream?dataset=<NODE_NAME>`: Returns a JSON object `{"downstream": [...]}` containing a deduplicated, lexicographically sorted array of all descendant nodes (datasets that depend on this node, directly or transitively). If the node has no downstream dependencies or doesn't exist, return an empty array.

Constraints:
- Your API must run on `127.0.0.1:8000`.
- The server must remain running in the background after you finish your interactions.
- You must handle transitive/recursive relationships correctly. For example, if A -> B and B -> C, then querying `/upstream?dataset=C` must return `["A", "B"]`.

Once you have verified your API is working correctly, you can exit.