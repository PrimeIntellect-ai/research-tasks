You are a Database Reliability Engineer managing a corrupted backup system. An automated backup verification job is failing due to a massive memory spike caused by a flawed SQL query, and we need to expose the corrected data and network routing information to a recovery service.

You have been provided with:
1. `/app/backup_metadata.db`: An SQLite3 database containing tables for `backups`, `data_centers`, and `network_links`.
2. `/app/schema_diagram.png`: An image of the original whiteboarding session that contains the critical schema join conditions and the designated 'Recovery Key' text.
3. `/app/report.sql`: A SQL query meant to list backup statuses, but it currently returns incorrect results due to an implicit cross-join.

Your objectives:
1. **Data Model Reverse Engineering & OCR**: Extract the text from `/app/schema_diagram.png` (using `tesseract` or similar). Use the join conditions specified in the image to fix the query in `/app/report.sql` so that it correctly joins `backups` and `data_centers` without an implicit cross-join. Apply the 'Recovery Key' found in the image as a `WHERE` clause filter on the backups table's `encryption_key` column.
2. **Graph Traversal**: The `network_links` table represents a graph of connections between data centers (`source_dc`, `target_dc`, `latency_ms`). You must write a Python function to compute the shortest path (lowest total latency) between two given data centers.
3. **API Service Implementation**: Create a Python HTTP API (e.g., using FastAPI, Flask, or simple HTTP server) that listens on `127.0.0.1:8000`. The API must have the following endpoints:
   - `GET /api/report`: Executes your fixed SQL query against `/app/backup_metadata.db` and returns a JSON array of objects. The schema must strictly validate against: `{"backup_id": str, "dc_name": str, "status": str}`.
   - `GET /api/route?src=<source_dc>&dst=<target_dc>`: Traverses the graph from the DB and returns a JSON object: `{"path": ["DC1", "DC2", ...], "total_latency": int}`.

Run your Python server in the background so that automated network tests can verify the endpoints. Keep the server running on `127.0.0.1:8000`.