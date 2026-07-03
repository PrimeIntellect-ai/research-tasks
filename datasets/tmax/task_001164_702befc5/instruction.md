You are a data engineer tasked with building a graph analytics ETL pipeline and serving the results via a local API. We are migrating our financial transaction data from a NoSQL document store to a graph representation to analyze money flow, compute centralities, and aggregate cluster volumes.

You have been provided with an image containing system configuration at `/app/config.png`. A daily dump of NoSQL transaction logs is located at `/home/user/transactions.jsonl`. 

Your goal is to build an automated pipeline that processes this data and exposes the analytics via a REST API.

**Step 1: Configuration Extraction**
Extract the API authentication token from the image located at `/app/config.png`. The image contains printed text. You will need to use OCR (e.g., `tesseract`) to read it. Look for a line in the format `AUTH_TOKEN: <token_value>`.

**Step 2: Graph ETL and Projection**
Read the transaction logs from `/home/user/transactions.jsonl`. Each line is a JSON object with `sender`, `receiver`, and `amount` fields.
Project this data into a directed graph where:
- Nodes represent entities (`sender` or `receiver`).
- Edges represent transactions from `sender` to `receiver`.
- The edge weight is the `amount` of the transaction. (If multiple transactions exist between the same sender and receiver, aggregate their amounts by summing them into a single edge).

**Step 3: Graph Analytics**
Using the projected graph, compute the following:
1. **PageRank Centrality**: Calculate the PageRank of all nodes using the edge weights. Use standard parameters (e.g., `alpha=0.85` in NetworkX, treating 'amount' as the weight). 
2. **Cluster Aggregation**: Find all weakly connected components in the graph. Identify each component by its lexicographically smallest node ID (e.g., if a component contains nodes "C", "A", and "Z", the cluster ID is "A"). Calculate the total transaction volume (sum of all edge amounts) within each component.

**Step 4: Serve the Results**
Create a Python web service (using Flask, FastAPI, or standard library) that listens on `127.0.0.1:8080`.
The API must require an `Authorization: Bearer <token_value>` header for all analytics endpoints, using the token extracted in Step 1.

Implement the following endpoints:
1. `GET /health`
   - Requires NO authentication.
   - Response: HTTP 200, JSON `{"status": "ok"}`
2. `GET /pagerank/<node_id>`
   - Requires Bearer token authentication. Returns HTTP 401 if missing or invalid.
   - Response: HTTP 200, JSON `{"node": "<node_id>", "pagerank": <float_value>}`
3. `GET /cluster/<cluster_id>`
   - Requires Bearer token authentication. Returns HTTP 401 if missing or invalid.
   - Response: HTTP 200, JSON `{"cluster": "<cluster_id>", "total_volume": <float_value>}`

**Execution:**
Write the necessary Python scripts and execute them. Keep the web server running on port 8080 in the background (or in a detached state) so that our automated verifier can issue HTTP requests to it. You may install dependencies like `networkx`, `flask`, `pytesseract`, `Pillow` using pip.