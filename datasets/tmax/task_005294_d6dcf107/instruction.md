You are a log analyst investigating a recent series of microservice outages. You need to build a C-based analysis engine that processes a large stream of logs, detects bursts of server errors, formats an incident report using a template, and serves the latest report via an HTTP API.

You have been provided with a workspace in `/app/`. Here is your objective:

1. **Fix the HTTP Library**: We are using the `mongoose` HTTP library (version 7.11) vendored at `/app/mongoose-7.11`. The previous engineer left a broken `Makefile` (it fails to compile on our Linux environment due to an incorrect compiler flag). Identify and fix the perturbation so you can compile `mongoose.c` and `mongoose.h` into a static library or object file.

2. **Process the Log Stream**: There is a large log file at `/app/logs/microservice.log`. 
   Format: `<UNIX_TIMESTAMP> <IP_ADDRESS> <HTTP_STATUS> <LATENCY_MS>` (space-separated).
   Write a C program (`/app/analyzer.c`) that streams this file efficiently (do not load the entire file into memory). 
   - Calculate a **rolling 60-second window** count of HTTP 5xx errors (HTTP status >= 500).
   - An "incident" is triggered whenever the 5xx error count in any 60-second window (inclusive of the current timestamp and the preceding 59 seconds) reaches **10 or more**.
   - For each incident, keep track of the *first 3 distinct IP addresses* that produced a 5xx error within that specific window. (This is your sampled data).

3. **Generate Reports via Template**: For the incident with the **highest absolute count of 5xx errors** across the entire log file (if there's a tie, pick the one that occurred at the latest timestamp), generate an HTML report.
   Read the template at `/app/templates/report.html.tmpl`.
   Replace the following exact placeholders:
   - `{{PEAK_TIME}}` -> The timestamp at the end of the window.
   - `{{ERROR_COUNT}}` -> The number of 5xx errors in that window.
   - `{{SAMPLED_IPS}}` -> A comma-separated list of the 3 sampled IPs (e.g., `192.168.1.1, 10.0.0.5, 172.16.0.2`).

4. **Serve the Data**: Use the fixed `mongoose` library in your C program to start an HTTP server listening on `0.0.0.0:8080`.
   - When a client issues a `GET /latest_incident` request, the server must respond with `200 OK` and the exact HTML string generated in Step 3.
   - Ensure the server runs continuously in the background so our automated systems can query it.

Compile your program, start it in the background, and ensure it is listening on port 8080.