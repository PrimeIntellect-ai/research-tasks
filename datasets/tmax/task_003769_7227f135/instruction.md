You are acting as a Site Reliability Engineer (SRE). A critical monitoring server crashed due to a sudden power loss, leaving our uptime database corrupted and our monitoring daemon crashing intermittently. You must recover the system and bring our metrics API back online.

Here is your to-do list:

1. **Recover the Admin Token**: The only record of the master API token is in a screenshot of an old Jira ticket saved at `/app/ticket_screenshot.png`. Extract the text from this image to find the token (look for a string like `API_KEY=...`). You will need this to secure the API.

2. **Recover the Database**: 
   In `/app/data/`, you will find `metrics.db.corrupt` and `metrics.db-wal`. The main database file is damaged, but the Write-Ahead Log (WAL) contains the latest uptime records. Recover the data and create a clean SQLite database at `/app/data/metrics_recovered.db`. The database contains a table `uptime` with columns `hostname` and `uptime_percentage`.

3. **Debug the Intermittent Failure**:
   The API server source code is located at `/app/api_server.py`. It has an intermittent crashing bug related to how it processes recent health-check requests. Use an interactive debugger or reproduce the failure to identify why it crashes on the 3rd or 4th request. Fix the bug in `/app/api_server.py`.

4. **Bring up the Service**:
   Start the fixed API server on `0.0.0.0:8080`. 
   The server must implement:
   - `GET /health` -> returns `{"status": "ok"}` (no authentication required)
   - `GET /metrics/<hostname>` -> returns `{"hostname": "<hostname>", "uptime": <value>}`. This endpoint MUST require an `Authorization: Bearer <API_KEY>` header using the key you recovered from the image.

Ensure the server is running as a background process or blocking in the terminal so it can be verified.