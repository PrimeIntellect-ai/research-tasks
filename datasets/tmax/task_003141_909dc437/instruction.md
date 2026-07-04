You are a storage administrator responsible for a centralized backup intake system. Recently, your storage cluster has been filling up rapidly due to corrupted, malicious, and misformatted backup archives being uploaded by malfunctioning clients. You need to fix the intake pipeline and create a robust bash worker to sanitize the incoming files and reclaim/protect disk space.

The system relies on three services running in user-space:
1. **Redis**: Runs on port `6379` (used as a message queue).
2. **Flask API**: An intake API located at `/app/api/intake.py` that receives uploads, saves them to `/home/user/staging/<uuid>/`, and pushes the directory path to a Redis list named `intake_queue`.
3. **Nginx**: Acts as a reverse proxy on port `8080`, routing traffic to the Flask API on port `8081`. 

Your task consists of two parts: Service Configuration and Worker Implementation.

**Part 1: Service Configuration**
- The Nginx configuration at `/home/user/nginx/nginx.conf` is currently rejecting legitimate large backups. Modify it to allow client uploads up to `20M`.
- The Flask application at `/app/api/intake.py` has a misconfigured Redis connection string. Fix it so it connects to the local Redis instance on port `6379`.
- Start all three services in the background (Redis, Nginx using your local config, and the Flask API).

**Part 2: The Sanitizer Worker**
Write a Bash script at `/home/user/sanitizer.sh` that acts as a continuous worker daemon. It must loop and pop directory paths from the Redis list `intake_queue`.
For each path popped, the worker must evaluate the backup against strict criteria to determine if it is "clean" or "evil". 

A "clean" backup MUST meet ALL the following conditions:
1. The staging directory contains a `metadata.json` file.
2. The `metadata.json` is strictly valid JSON (parseable by `jq`).
3. The JSON contains a key `".backup_type"` exactly equal to `"system_state"`.
4. The staging directory contains a `payload.dat` file.
5. The `payload.dat` file must be a valid GZIP file. You MUST verify this by extracting the binary header (the first 2 bytes must be the magic bytes `1f 8b`).
6. The `payload.dat` file size must not exceed 10 Megabytes (10485760 bytes). 

If a backup is "clean":
- Atomically append the contents of `metadata.json` as a single line to `/home/user/archive/master_index.jsonl`. You MUST use `flock` on the index file to ensure concurrent workers do not corrupt the JSONL file.
- Move the `payload.dat` to `/home/user/archive/blobs/<uuid>.gz`.

If a backup fails ANY of the criteria (it is "evil"), you must aggressively reject it:
- Recursively delete the staging directory for that upload.

**Verification Phase**
Once your script is ready and services are running, an automated verifier will simulate heavy traffic by pushing an adversarial corpus of files (some clean, some highly malicious) through your Nginx endpoint. Your `sanitizer.sh` must process them successfully. Do not stop your script; leave it running so it can process the verifier's incoming test flow.