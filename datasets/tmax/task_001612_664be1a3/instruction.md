You are a data analyst working on network infrastructure analysis. We have an export of our network topology in CSV format, but the logic for calculating infrastructure cost metrics was left as a screenshot of a whiteboard by the previous engineer.

Your task is to process these CSVs, build a graph model, calculate the node metrics based on the whiteboard image, and expose a REST API to query the aggregated metrics.

Here are the resources you have:
1. `/app/nodes.csv` - Contains columns: `node_id`, `node_type`, `metric_a`, `metric_b`
2. `/app/edges.csv` - Contains columns: `source_id`, `target_id` (representing undirected connections)
3. `/app/cost_formula.png` - An image containing the text formulas for calculating the "base_cost" of a node based on its `node_type`. Use OCR to extract this logic.

Workflow:
1. Extract the cost formulas from `/app/cost_formula.png`.
2. Parse the CSV files and project them into an undirected graph.
3. Calculate the `base_cost` for each node using the extracted formulas.
4. Calculate the `neighborhood_cost` for each node. This is the sum of the `base_cost` of all nodes directly connected to it (its immediate neighbors).
5. Build and start a Python HTTP web server listening on `0.0.0.0:5050`.
6. Expose a GET endpoint at `/api/neighborhood/{node_id}`.
7. The endpoint must require an HTTP header `Authorization: Bearer net-graph-secret`.
8. The endpoint should return a JSON response exactly matching this format:
   `{"node_id": "A1", "neighborhood_cost": 150.5}`
   If the node is not found, return a 404 status code.

You may use Python with any standard libraries or pre-installed packages like `networkx`, `flask`, `fastapi`, `uvicorn`, `pytesseract`, and `Pillow`.

Keep the server running in the foreground or background once it is ready. Leave a file named `/tmp/server_ready` when your API is up and running.