You are acting as a capacity planner for our internal infrastructure. We are rolling out a new log ingestion and aggregation pipeline to track CPU and memory usage across our fleet, but the current deployment is partially broken and vulnerable to bad data. 

Your task is divided into three phases: Backup, Multi-Service Pipeline Repair, and Data Sanitization.

**Phase 1: Backup**
Before touching the system, create a backup of the existing historical capacity database.
Archive the directory `/app/data/history/` into a compressed tarball at `/home/user/history_backup.tar.gz`.

**Phase 2: Multi-Service Pipeline Repair**
Our log ingestion pipeline under `/app/services/` consists of three cooperating services:
1. Nginx (Reverse Proxy) - intended to listen on port 8080.
2. Capacity API (Flask) - intended to run on port 5000.
3. Redis (Message Queue) - intended to run on port 6379.

Currently, the end-to-end flow is broken. 
- You must modify `/app/services/nginx/nginx.conf` so that any HTTP POST request to `http://127.0.0.1:8080/ingest` is correctly proxy-passed to the Capacity API.
- For security (acting as a host-level firewall restriction), the Capacity API (`/app/services/api/app.py`) must only bind to `127.0.0.1`, not `0.0.0.0`. Modify the startup script or code to ensure this.
- Ensure all three services can be started successfully using the provided `/app/services/start_all.sh` script.

**Phase 3: Data Sanitization (Adversarial Corpus)**
Our metrics agents sometimes malfunction or get spoofed, sending impossible capacity data that crashes our planning models. 
Write a Python script at `/home/user/sanitizer.py` that reads JSON-lines (one JSON object per line) from standard input (`stdin`) and writes only the valid JSON-lines to standard output (`stdout`).

A capacity log line is only VALID if it meets ALL the following criteria:
- It is valid JSON.
- It contains exactly three keys: `host`, `cpu_percent`, and `mem_bytes`.
- `host` is a string containing only alphanumeric characters and hyphens (no spaces, no special characters, length between 3 and 64 characters).
- `cpu_percent` is a float or integer between 0.0 and 100.0 (inclusive).
- `mem_bytes` is an integer strictly greater than 0.

Any line failing these checks must be dropped (omitted from `stdout`). Valid lines must be printed exactly as they are structurally (you may re-serialize them with `json.dumps`).

We will test your script against two corpora located in `/app/corpora/`.