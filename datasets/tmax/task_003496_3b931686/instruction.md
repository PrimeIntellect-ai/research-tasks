You are a Database Reliability Engineer investigating a partial monitoring failure. The primary metrics database went down, but a legacy dashboard continued recording its screen. We have the screen recording of the dashboard in `/app/dashboard_recording.mp4`.

Your task is to extract the missed backup job IDs from the video, reconcile them with our relational inventory and NoSQL execution logs, and expose the recovered data via a lightweight HTTP API.

**Step 1: Extract Job IDs**
Analyze the video at `/app/dashboard_recording.mp4`. You will find text flashing on the screen with the pattern `JOB_ID: <4-character-alphanumeric>`. Use `ffmpeg` and `tesseract` to extract all unique Job IDs from the frames.

**Step 2: Data Reconciliation via Bash Querying**
You are provided with two data sources:
1.  **SQLite DB** (`/app/inventory.db`): Contains tables `jobs(id, server_id, expected_gb)` and `servers(id, hostname)`.
2.  **NoSQL JSONL Dump** (`/app/nosql_dump.jsonl`): Contains execution records, e.g., `{"job_id": "A100", "metrics": {"actual_gb": 45}, "status": "SUCCESS"}`.

Write a Bash script (e.g., `/home/user/query.sh`) that takes a `job_id` as an argument. The script must chain queries using `sqlite3` and `jq` to perform the following:
*   Perform a SQL JOIN to find the `hostname` and `expected_gb` for the given job.
*   Use a NoSQL aggregation pipeline equivalent (via `jq`) to extract the `actual_gb` and `status` from the JSONL dump.
*   Output the combined result as a single, flat JSON object:
    `{"job_id": "...", "hostname": "...", "expected_gb": <int>, "actual_gb": <int>, "status": "..."}`

**Step 3: Create a Query API**
Start an HTTP server listening on `127.0.0.1:8080`. You may use Python's `http.server` or `socat`/`nc` to handle the HTTP protocol, but it *must* execute your Bash data querying pipeline to fulfill requests.
*   The server must respond to `GET /?job=<job_id>`
*   The response must have a `200 OK` status and the Content-Type `application/json`.
*   The body of the response must be the JSON output from your Bash script.
*   The server must remain running in the background.

The automated verifier will issue HTTP requests to your server to validate the data for the extracted job IDs.