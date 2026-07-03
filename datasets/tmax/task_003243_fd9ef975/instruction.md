You are a Database Reliability Engineer (DBRE) investigating a backup storage inflation issue.

We have a system that tracks database backups, but a recent report indicates that the calculated storage size for corrupted backups is massively inflated. We believe there is a bug in the SQL query used to calculate these metrics, likely an implicit cross join somewhere in the schema relationships.

Additionally, the list of recently corrupted backup IDs was only captured in a video recording of a monitoring dashboard, as the original log stream was lost.

Your tasks:
1. **Extract Corrupted Backup IDs**:
   Analyze the video file located at `/app/corruption_report.mp4`. The video contains a scrolling terminal output. Extract the backup IDs marked as "CORRUPTED" (format: `BK-XXXX`). You may need tools like `ffmpeg` and `tesseract-ocr` to extract frames and read the text.

2. **Fix the Calculation Query**:
   There is a SQLite database at `/app/backup_meta.db` containing the schema for `servers`, `backups`, and `storage_nodes`.
   There is a Go service stub at `/app/server.go` which is supposed to calculate the total size of corrupted backups per server. However, the SQL query inside it is wrong and returns massively inflated sizes due to a bad join condition.
   Reverse engineer the schema in `/app/backup_meta.db`, fix the SQL query in `/app/server.go` so it properly joins the tables and correctly aggregates `size_bytes` per `hostname` for the corrupted backups without duplicating rows.

3. **Deploy the Service**:
   Modify `/app/server.go` to inject the corrupted backup IDs you extracted from the video into the fixed query.
   The Go service must run an HTTP server listening on exactly `127.0.0.1:8080`.
   It must expose a single endpoint: `GET /api/v1/corrupted_sizes`.
   The endpoint must return a JSON array of objects, sorted alphabetically by hostname, structured exactly like this:
   ```json
   [
     {
       "hostname": "prod-db-01",
       "total_corrupted_bytes": 1048576
     },
     ...
   ]
   ```

Start the Go server in the background so it remains running. The verification script will issue HTTP requests to `127.0.0.1:8080/api/v1/corrupted_sizes` to verify your work.