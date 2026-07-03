You are an ETL data engineer. We have an SQLite database located at `/app/data.db` containing e-commerce data, but the pipeline has been producing incorrect graph analytics due to some undocumented business rules and potentially stale data from corrupted indexes.

Your task is to fix the data extraction, compute the correct graph metrics, and serve the result via a local HTTP API.

1. **Schema and Rules**: There is an image file at `/app/business_rules.png`. It contains a flowchart/text that specifies exactly which records to filter out before processing, and which graph centrality metric to compute for our vendors. You must read this image to understand the correct filtering rules and the exact metric required.
2. **Database operations**: The database has tables `clients`, `vendors`, and `sales`. There is a known issue where an existing index on the `sales` table might be corrupted, returning stale or duplicate rows. You should safely rebuild or reindex the database before querying.
3. **Graph Analytics**: Based on the rules extracted from the image, compute the specified centrality metric for each vendor using the cleaned relational data. 
4. **Data Serving**: Write and run a Python HTTP server (e.g., using Flask or FastAPI) that listens on `127.0.0.1:8000`. It must expose a `GET /centrality` endpoint.
   - The endpoint must return a JSON response with the computed metrics.
   - Format: A JSON dictionary where keys are vendor IDs (as strings) and values are their computed centrality scores (as integers). Example: `{"1": 5, "2": 3}`.

Ensure your server remains running in the foreground or background so that our automated systems can query it. Do not hardcode the data; your script must query `/app/data.db` dynamically.