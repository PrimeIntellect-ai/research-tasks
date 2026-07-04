You are a data analyst working with a newly extracted dataset of user interactions and profiles, stored as CSV files. Your goal is to process these CSVs, perform graph analytics and document aggregations, and expose the results via a local HTTP API.

1. **Information Extraction**:
There is an image file located at `/app/query_params.png`. It contains the parameters for our primary graph query (specifically, a Target Node ID and a Search Depth). Use OCR (e.g., `tesseract`) to extract these values. 

2. **Data Processing**:
You have two CSV files: `/home/user/data/nodes.csv` and `/home/user/data/edges.csv`.
- `nodes.csv` contains `node_id` and `profile_data` (a JSON string representing a document).
- `edges.csv` contains `source`, `target`, and `interaction_type`.

Using Python, write a script that loads this data into memory (you can use libraries like `networkx` for graph operations). 

3. **HTTP API Service**:
Create a Python-based HTTP server (e.g., using `Flask`, `FastAPI`, or the built-in `http.server`) that listens on `127.0.0.1:8080`.

It must expose the following endpoints:
- `GET /api/target_neighborhood`
  Returns a JSON array of all `node_id`s that are within the Search Depth of the Target Node ID extracted from the image. The distance is calculated based on shortest path ignoring edge direction. Return the list sorted alphabetically.
  
- `GET /api/aggregate?interaction_type=<type>`
  Simulate a NoSQL aggregation pipeline: Find all edges matching the given `interaction_type`. Identify all unique `source` nodes for these edges. Parse their `profile_data` JSON. Calculate the average of the `age` field across these source nodes. Return a JSON object: `{"average_age": <float_value>}`. Round to 2 decimal places.

Run your server in the background so it is available for testing. Do not exit the server once started. You may install any Python packages you need (like `networkx`, `flask`, `pytesseract`, `Pillow`).