You are an observability engineer tuning a local telemetry data pipeline for your dashboards. Since you are in a constrained environment, you need to build the pipeline using Git, Python, and shell tools.

Your objective is to build an end-to-end local telemetry ingestion pipeline and simulate data flow. Follow these requirements precisely:

1. **Simulated Dashboard Ingest Servers**: 
   Write a Python script (`/home/user/backend.py`) and launch two instances of it on ports `8081` and `8082`. 
   These servers must accept HTTP POST requests containing JSON payloads. When a request is received, the server should append the raw JSON body to a log file named `/home/user/metrics_<PORT>.log` (e.g., `metrics_8081.log`), with one JSON object per line.

2. **Python Load Balancer**:
   Write a Python script (`/home/user/lb.py`) that acts as a reverse proxy and load balancer. 
   It must listen on `127.0.0.1:8080`. It should accept HTTP POST requests and forward them in a strict round-robin fashion to the two backend servers (`127.0.0.1:8081` and `127.0.0.1:8082`). 
   The load balancer must inject an HTTP header `X-Forwarded-By: ObservabilityLB` into the forwarded request.

3. **Telemetry Git Server & Hook**:
   Create a bare Git repository at `/home/user/telemetry.git`.
   Write a `post-receive` Git hook in Python (`/home/user/telemetry.git/hooks/post-receive`). Ensure it is executable.
   When a developer pushes to this repository, the hook must process all new commits. For each commit, the hook must:
   - Extract the commit author's name.
   - Calculate the total number of inserted lines in that commit (using standard git diff/show statistics).
   - Construct a JSON payload exactly formatted as: `{"author": "Author Name", "lines_added": <integer>}`
   - Send this payload as an HTTP POST request to your load balancer at `http://127.0.0.1:8080`.

4. **Data Simulation**:
   Clone the bare repository to `/home/user/telemetry-clone`.
   Simulate developer activity by creating three separate commits in the clone:
   - Commit 1: Author "Alice", adding exactly 5 lines of text to a new file `app.py`.
   - Commit 2: Author "Bob", adding exactly 10 lines of text to `app.py`.
   - Commit 3: Author "Alice", adding exactly 15 lines of text to `app.py`.
   Push these commits to the bare repository `origin master` in a single push operation so the hook processes them.

5. **Text Processing Pipeline**:
   After the push, use standard text processing tools (`awk`, `sed`, `grep`) to parse both `/home/user/metrics_8081.log` and `/home/user/metrics_8082.log`.
   Calculate the total number of `lines_added` across all commits authored by "Alice".
   Output the final result to `/home/user/dashboard-summary.txt` in the exact format: `TOTAL_ALICE=<number>`.

Ensure all background Python services are left running when you are done.