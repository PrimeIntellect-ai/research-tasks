You are a capacity planner analyzing system resource usage. You need to set up a pipeline to continuously monitor the system's process count, serve this metric via a vendored local metrics server, and expose a custom TCP aggregator for a centralized monitoring system to query.

Here is your task:

1. **Fix and Deploy the Vendored Package**:
   We have vendored a simple metrics web server at `/app/vendor/metrics_server-1.0.0`. 
   - However, the source code in `/app/vendor/metrics_server-1.0.0/server.py` has a deliberate hardcoded port error (it tries to bind to the privileged port 80). 
   - You must fix the code so that it binds to the port specified by the `METRICS_PORT` environment variable (falling back to 8000 if not set).
   - Start this server as a background process listening on port `9090`. It is designed to read and serve the contents of `/home/user/stats.json` whenever it receives an HTTP GET request.

2. **Automated Data Collection**:
   - Write a Python script at `/home/user/gather_stats.py` that counts the total number of running processes on the system (e.g., using `ps -e`).
   - The script must write this integer count to `/home/user/stats.json` in exact JSON format: `{"process_count": <integer>}`.
   - Run this script once immediately to populate the file.
   - Configure a user cron job to run `/home/user/gather_stats.py` every minute.

3. **Custom TCP Aggregator**:
   - Write and run a Python TCP server script at `/home/user/aggregator.py` that listens on `127.0.0.1` port `8080`.
   - When a client connects via TCP and sends the exact ASCII string `FETCH_CAPACITY` (with or without a trailing newline), the aggregator must:
     a) Make an HTTP GET request to `http://127.0.0.1:9090/`.
     b) Parse the JSON response.
     c) Send back the exact string `CAPACITY_OK: <integer>\n` over the TCP connection (where `<integer>` is the process count read from the JSON) and close the connection.
   - Start this aggregator in the background.

Constraints:
- Ensure both the metrics server (port 9090) and the aggregator (port 8080) are running continuously.
- Use only standard Python libraries and standard Linux tools. Do not install external libraries.