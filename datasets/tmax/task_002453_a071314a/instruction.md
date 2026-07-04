You are tasked with optimizing and reconfiguring our local Artifact Manager, which curates large binary repositories. The system currently suffers from massive storage bloat due to duplicate binary artifacts across different versions, and its multi-service stack is currently broken.

The environment contains three components located in `/app/`:
1. A Flask backend (`/app/backend/app.py`) running on port 5000 that serves the artifacts.
2. An Nginx reverse proxy configured via `/app/nginx/nginx.conf` that should listen on port 8080 and forward traffic to the Flask backend.
3. A Redis instance on port 6379 used for caching artifact metadata.

Your tasks are:

**Phase 1: Service Glue & Reconfiguration**
The startup script `/app/start.sh` starts all services, but the end-to-end flow is broken. Nginx is misconfigured and returns 502 Bad Gateway because it is pointing to the wrong upstream port, and the Flask app fails to connect to Redis because it is looking for a socket instead of the local port. 
1. Modify `/app/nginx/nginx.conf` to correctly proxy requests to `127.0.0.1:5000`.
2. Modify `/app/backend/.env` (or the environment variables in the Flask app) so the `REDIS_URL` points to `redis://127.0.0.1:6379/0`.
3. Restart the services using `/app/start.sh`. Ensure that a `curl http://127.0.0.1:8080/health` returns `{"status": "ok"}`.

**Phase 2: Artifact Deduplication (The Curation Script)**
Write a Python script `/home/user/curate.py` that traverses the primary artifact repository located at `/app/data/artifacts/`.
1. The directory contains deeply nested binary files (e.g., `.bin`, `.so`, `.jar`).
2. Identify duplicate files based on their SHA-256 content hashes.
3. Keep the oldest file (based on file creation/modification metadata) as the master copy.
4. Replace all other identical files with **hard links** to the master copy to save disk space.
5. Create an incremental backup log at `/app/data/backup_index.json` containing a JSON dictionary mapping the relative path of every file in the repository to its SHA-256 hash.

**Requirements**:
- The script must use Python and handle large files efficiently (read in chunks).
- Run your script. The success of the deduplication will be evaluated by measuring the total disk usage of `/app/data/artifacts/` using physical block allocation (i.e., hardlinks will significantly reduce the consumed space). 
- Leave the services running so the evaluation script can test the HTTP artifact retrieval protocol flow.