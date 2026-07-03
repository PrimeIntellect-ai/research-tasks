You are a Database Reliability Engineer (DBRE) responsible for managing a multi-service backup infrastructure. We are rolling out a new backup architecture, but currently, the system is failing for two reasons: a misconfigured service topology, and a lack of input validation causing the backup workers to crash on malformed payloads.

Your task is divided into two parts:

**Part 1: Fix the Service Topology**
The infrastructure located in `/app/` consists of four services:
- Nginx (reverse proxy, intended to run on port 8080)
- Python Backup API (runs on port 8000)
- PostgreSQL (metadata DB, port 5432)
- Redis (job queue, port 6379)

Currently, the services start (via `/app/start_services.sh`), but the end-to-end flow is broken. 
1. Edit `/app/nginx.conf` so that any request to `/api/` is proxied to the Python Backup API at `127.0.0.1:8000`.
2. Edit the environment variables in `/app/backend/.env` so the Backup API can properly connect to PostgreSQL (user: `backup_user`, pass: `secret`, db: `backups`) and Redis (host: `127.0.0.1`, port: `6379`).
When fixed, `curl http://localhost:8080/api/health` should return a `200 OK` status with `{"status": "healthy"}`.

**Part 2: Build the Payload Sanitizer**
The Backup API receives JSON payloads that specify backup extraction queries and their table dependency graphs. Malicious or malformed payloads are crashing the system. 

Write a C program located at `/home/user/sanitizer.c` and compile it to `/home/user/sanitizer`.
This program must read a JSON string from `stdin` until EOF, parse it, and print exactly `ACCEPT\n` or `REJECT\n` to `stdout`.

To help you parse JSON in C, the `cJSON` library is provided at `/home/user/cJSON/cJSON.h` and `/home/user/cJSON/cJSON.c`.

The sanitizer must `REJECT` the payload if ANY of the following rules are violated, otherwise `ACCEPT`:
1. **Schema Validation:** The JSON must be an object containing exactly these fields:
   - `backup_id` (integer)
   - `query` (string)
   - `deps` (array of arrays, where each inner array contains exactly two integers representing a directed dependency edge `[from_node, to_node]`).
2. **Parameterized Query Check:** To prevent SQL injection, the `query` string must NOT contain any single quote characters (`'`). It must rely entirely on parameterized placeholders (like `$1` or `?`).
3. **Graph Traversal (Acyclic Check):** The `deps` array defines a dependency graph for backup ordering. The graph MUST be a Directed Acyclic Graph (DAG). If the graph contains any cycles (e.g., node 1 depends on 2, and 2 depends on 1), you must reject it.

Compile your code with:
`gcc /home/user/sanitizer.c /home/user/cJSON/cJSON.c -o /home/user/sanitizer -I/home/user/cJSON`

Ensure your sanitizer works flawlessly. It will be tested against a hidden corpus of clean and evil payloads.