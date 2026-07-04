You are tasked with completing the migration of a legacy telemetry system from Python 2 to Python 3. The system consists of a WebSocket server, a SQLite database, an Nginx reverse proxy, and a Node.js end-to-end test suite. The initial migration attempt left several issues that you must fix.

Your workspace is located at `/home/user/telemetry_system`.

1. **Code Quality & Memory Debugging**:
   The provided Python server script (`/home/user/telemetry_system/server.py`) was partially migrated to Python 3 using the `websockets` and `asyncio` libraries. However, it contains legacy Python 2 syntax (e.g., old print statements) that prevents it from running. Furthermore, the original developer noted a severe memory leak: the server stores every incoming message in a global list without bounds. 
   - Fix the syntax errors so it runs under Python 3.
   - Fix the memory leak by ensuring the server does not store incoming messages in memory indefinitely (it should only insert them into the database).
   
2. **Schema Migration**:
   The database `/home/user/telemetry_system/db.sqlite3` currently has a table named `telemetry` with columns `id INTEGER PRIMARY KEY`, `data TEXT`. 
   - Apply a schema migration to rename the table to `device_telemetry` and add a new column `received_at DATETIME DEFAULT CURRENT_TIMESTAMP`.

3. **Reverse Proxy Configuration**:
   Create an Nginx configuration file at `/home/user/telemetry_system/nginx.conf`.
   - It should listen on port `9000`.
   - It must route requests to the `/ws` endpoint to the Python WebSocket server running on `127.0.0.1:8080`.
   - Ensure the configuration correctly upgrades the connection to support WebSockets.
   - Run Nginx as a non-root user using this configuration.

4. **End-to-End Test Orchestration**:
   Write a Node.js script at `/home/user/telemetry_system/run_e2e.js` that uses the `ws` library to:
   - Connect to `ws://127.0.0.1:9000/ws`.
   - Send exactly 5 telemetry messages (e.g., `{"sensor": "temp", "value": 22}`).
   - Disconnect.
   - Query the `device_telemetry` table in `/home/user/telemetry_system/db.sqlite3` to verify exactly 5 records exist.
   - If successful, write the string `E2E_PASS` to `/home/user/telemetry_system/e2e_result.log`.

Make sure to install any necessary dependencies (e.g., `ws` via npm, `websockets` via pip) locally or globally as appropriate. Start the Python server and Nginx before running your test.