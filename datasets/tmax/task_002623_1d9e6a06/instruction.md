You are helping a researcher organize and analyze a complex dataset of relationships. The researcher has provided an image with some specific analytical parameters, a raw dataset of node relationships, and a buggy script that currently fails to process the data correctly.

Here is what you need to do:

1. **Extract Parameters:** Read the image located at `/app/task_req.png`. It contains the specific graph centrality metric and its parameter that the researcher wants to calculate. (You may use OCR tools like `tesseract` to read it).

2. **Fix the Data Processing:** The researcher has a NoSQL-style JSON lines dataset at `/app/dataset.jsonl`. Each line is a document containing a source node and a list of destination nodes (e.g., `{"src": "NodeA", "dst": ["NodeB", "NodeC"]}`). There is a script at `/home/user/process.py` that is supposed to parse this dataset into a directed graph and compute the required centrality metric. However, the script contains a logical flaw (similar to an implicit cross join) that adds incorrect edges between all nodes, ignoring the actual `dst` arrays. Fix the script so it correctly builds the graph using *only* the edges explicitly defined in the `dst` arrays.

3. **Compute Graph Analytics:** Update the script to compute the graph metric specified in the image using the `networkx` Python library. Ensure you use the exact parameter values extracted from the image. 

4. **Serve the Results:** The agent must create and start an HTTP server listening on `127.0.0.1:8080`. 
   - The server must respond to `GET /metric` requests.
   - The response must be a JSON object mapping node names to their computed centrality scores, formatted to 4 decimal places.
   - Example expected response format: `{"NodeA": 0.1234, "NodeB": 0.5678}`.

Keep the server running in the background so the verification system can query it. You may use any standard Python HTTP server libraries (like `http.server`, `Flask`, or `FastAPI`).