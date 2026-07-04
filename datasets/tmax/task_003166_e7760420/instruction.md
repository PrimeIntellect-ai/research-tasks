You are a Platform Engineer maintaining a CI/CD pipeline for a secure Python web backend. The pipeline has completely halted due to several intertwined failures involving a native C library, an outdated database schema, and a failed UI security test whose results are locked inside a video artifact.

Your objective is to fix the build, perform the database schema migration, extract the required security credentials from the test video, and bring up the backend API securely.

Here are the specific steps you must complete:

**Phase 1: Fix the C Library Build System**
The Python backend relies on a custom C authentication module located at `/home/user/auth-lib/`.
Currently, running `make` fails with a linking error because it attempts to build `libauth.so` but fails to properly link the standard Math and Crypto libraries, and it has a syntax error in the Makefile regarding positional arguments.
1. Fix the `Makefile` in `/home/user/auth-lib/` so that running `make` successfully produces `libauth.so`.
2. Ensure the resulting shared object can be successfully loaded by the Python script `/home/user/auth-lib/test_load.py` (which you can run to verify).

**Phase 2: Perform the Database Schema Migration**
The application uses an SQLite database located at `/home/user/db/audit.db`.
The current schema (Version 1) has a table `log_entries` with columns: `id` (INTEGER PRIMARY KEY), `action` (TEXT), `timestamp` (INTEGER).
You must write a Python script to migrate this database to Version 2 by enforcing new web security constraints:
1. Add a new column `client_ip` (TEXT).
2. Set `client_ip` to `"0.0.0.0"` for all existing records.
3. Create a new table `users` with columns: `user_id` (INTEGER PRIMARY KEY), `username` (TEXT).
4. Insert a default user into `users`: `(1, 'admin')`.
5. Modify `log_entries` to include a `user_id` (INTEGER) column that acts as a Foreign Key referencing `users(user_id)`. Update all existing logs to have `user_id = 1`.
*Note: SQLite requires creating a new table and copying data to alter tables with new foreign key constraints.*

**Phase 3: Video Artifact Analysis**
An automated UI security test failed, and the only artifact left is a video recording located at `/app/ci_test_run.mp4`.
1. The video contains a sequence of UI testing frames. Somewhere in the video (between seconds 2 and 4), a QR code flashes on the screen containing a dynamically generated API Authorization Token.
2. Use `ffmpeg` (preinstalled) to extract the frames and write a Python script (you may install `pyzbar` and `Pillow` via pip) to scan the frames, locate the QR code, and decode the text. 
3. Save the decoded string. This string is your `BEARER_TOKEN`.

**Phase 4: Bring up the API Service**
Write a Python web service (using Flask or FastAPI, which you may install via pip) that binds to `127.0.0.1:8000`.
The service must implement the following REST API:
1. `GET /health`: Returns HTTP 200 with JSON `{"status": "ok"}`.
2. `GET /api/v1/audit/logs`: 
   - **Authentication:** Must strictly require the HTTP header `Authorization: Bearer <BEARER_TOKEN>` (using the token you extracted from the video). If missing or invalid, return HTTP 401.
   - **Response:** If authenticated, query the migrated `/home/user/db/audit.db` and return HTTP 200 with a JSON array of all log entries. The JSON format for each entry must be: 
     `{"id": 1, "action": "...", "timestamp": 123456, "client_ip": "...", "user_id": 1}`.

Keep this service running in the foreground so the automated verifier can test it.