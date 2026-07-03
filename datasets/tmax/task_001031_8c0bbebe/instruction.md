You are a Site Reliability Engineer managing a staged rolling deployment of a local application suite.

Currently, our deployment script `/home/user/deploy/deploy.py` is failing. It attempts to launch three worker processes concurrently, but these workers have strict start-up dependencies, similar to missing `After=` directives in systemd. 

Worker 2 depends on Worker 1, and Worker 3 depends on Worker 2. 
If a worker starts before its dependency is fully ready, it crashes immediately.

A worker is only considered "ready" when:
1. It has created its readiness file (`/home/user/deploy/w<ID>.ready`).
2. It is successfully listening on its assigned local port (Worker 1: 8081, Worker 2: 8082, Worker 3: 8083).

Your task is to rewrite `/home/user/deploy/deploy.py` in Python to act as a proper staged deployment automation script. 

The updated `deploy.py` must:
1. Start Worker 1 (`python3 /home/user/deploy/worker.py 1`).
2. Continuously poll the filesystem to check if `/home/user/deploy/w1.ready` exists, AND perform a connectivity diagnostic to verify that local port 8081 is accepting connections.
3. Once both conditions are met for Worker 1, proceed to start Worker 2.
4. Repeat the filesystem and connectivity checks for Worker 2 (file: `w2.ready`, port: 8082).
5. Start Worker 3 and repeat the checks (file: `w3.ready`, port: 8083).
6. Once Worker 3 is fully verified as ready, the script must write the exact string `DEPLOYMENT SUCCESSFUL` to a new log file at `/home/user/deploy/status.log` and exit gracefully.

Constraints:
- Do not modify `/home/user/deploy/worker.py`.
- You must use Python to write the updated `deploy.py`.
- Make sure to leave the background worker processes running when `deploy.py` exits.