You are tasked with acting as a database administrator and backend developer to fix a corrupted graph database and implement a query service.

We have an SQLite database located at `/app/graph.db` containing a social network graph. The database has two tables:
- `nodes` (id INTEGER PRIMARY KEY)
- `edges` (src INTEGER, dst INTEGER)

Due to a past migration error, the `edges` table contains duplicate records (stale/duplicate rows that should have been unique). 

Your tasks are:
1. **Database Cleanup**: Deduplicate the `edges` table in `/app/graph.db` such that every `(src, dst)` pair is unique. 
2. **Understand the Query Requirement**: There is an image at `/app/task.png` containing a specific graph analytics query requirement. You will need to extract the text from this image to understand what analytics to perform. Tesseract OCR is installed (`tesseract /app/task.png stdout`).
3. **Build a Service**: Write a Go application (in `/app/server.go`) that connects to the cleaned SQLite database and starts an HTTP server listening on exactly `127.0.0.1:9000`.
4. **Implement the Endpoint**: The server must expose a `POST /analyze` endpoint. It will receive a JSON payload like `{"node_id": 1}`. It must execute the graph query described in the image for the given `node_id`, and return a JSON response matching the structure requested in the image.

Ensure your Go server runs continuously in the foreground or background once started, as our automated test suite will send real HTTP POST requests to `http://127.0.0.1:9000/analyze` to verify your implementation.