PagerDuty Alert - 03:14 AM
SEVERITY: CRITICAL
SERVICE: `realtime-aggregator`
ISSUE: The primary `compute_engine` daemon crashed, causing cascading timeouts in the `frontend_api`. On-call engineers attempted to restart the system, but the `compute_engine` fails to build from the `main` branch, and the staging binary fails to start due to a corrupted Write-Ahead Log (WAL).

You are the primary on-call engineer. You need to restore the system to a healthy state. 

System Architecture & Services:
The system is located in `/app/` and consists of three components running locally:
1. `state_db`: Redis server running on `127.0.0.1:6379`.
2. `compute_engine`: A custom C daemon running on `127.0.0.1:9000`. It processes requests and writes to a local WAL at `/app/data/engine.wal`.
3. `frontend_api`: A Python Flask app running on `127.0.0.1:8080` that routes traffic to the compute engine.

Your tasks:
1. **Database Recovery**: The previous crash corrupted `/app/data/engine.wal`. The C daemon refuses to start, throwing a "WAL tail corruption" error. Diagnose the file (records are 32 bytes each, starting immediately after a 16-byte header) and truncate the corrupted, incomplete record at the end.
2. **Build Failure Fix**: The `compute_engine` repository at `/app/compute_engine/` (a Git repository) fails to compile on the latest `main` branch. Fix the build failure.
3. **Regression & Concurrency Fix**: Once running, the system will experience a severe livelock under load. Use `git bisect` to identify the regression. There is a boundary condition / off-by-one error in the worker thread ring-buffer (`queue.c`) that causes threads to spin indefinitely under high contention, ruining convergence. Fix the C code so it handles contention correctly.
4. **Integration & Bring-up**: Use `/app/start_services.sh` to start Redis, the C daemon, and the Flask API.

Validation:
Once you believe the system is fixed, run the load test script:
`python3 /app/load_test.py`
This script sends 10,000 requests to `http://127.0.0.1:8080/process`. 

Your goal is for the system to process the requests successfully and achieve a total execution time of LESS THAN 3.0 seconds (which indicates the contention bug is resolved). Keep tweaking your C code and restarting the services until you meet this performance threshold.