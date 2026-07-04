You are an operations engineer tasked with triaging a broken data ingestion pipeline. The pipeline processes log payloads and saves them to a database. Recently, the pipeline has stalled, and incident reports indicate multiple failures.

The architecture consists of:
1. An injection script (`/app/inject.py`) that reads raw JSON payloads from `/app/data/payloads.jsonl` and sends them via HTTP POST to the API.
2. A Flask API (Service A) running on port 5000 that receives payloads and pushes them to a Redis queue.
3. Redis (Service B) running on port 6379.
4. A Python Worker (Service C) running in the background that pops payloads from Redis, processes them, and saves them to an SQLite database at `/app/data/processed.db`.

You have three primary objectives to resolve the incident:

1. **Authentication Failure (Git Forensics):** The `inject.py` script is receiving 401 Unauthorized errors from the API. The hardcoded API token was recently removed from the API's configuration for security reasons and replaced with an environment variable requirement (`API_SECRET_TOKEN`). The original token value is lost, but it was committed in the git history of the `/app/api` repository before being removed. Find the token, configure the environment/API, and update `/app/inject.py` to use it so data can flow.
2. **Worker Crashes (Log Analysis & Error Recovery):** Once data reaches the worker, the worker process crashes repeatedly. Inspect the worker logs at `/app/worker/logs/worker.log` to diagnose the stack trace. 
3. **Corrupted Input Handling:** The `payloads.jsonl` file contains roughly 10,000 entries. A small fraction of these entries contain malformed, corrupted, or malicious fields (similar to a buffer overflow payload attempting to exploit a fragile C-extension parser downstream). Fix `/app/worker/processor.py` to gracefully catch these corrupted inputs, skip them, and continue processing the valid payloads without crashing.

**Steps to complete:**
- The services can be started using `/app/start_services.sh`. 
- You can restart the worker manually if you modify its code.
- Run `/app/inject.py` to push the data through the pipeline once you have fixed the issues.
- Your ultimate goal is to ensure the maximum possible number of valid payloads are processed and stored in `/app/data/processed.db`.

An automated verifier will check the completion of your task by calculating the recovery rate: the number of successfully processed valid records divided by the total number of valid records in the original dataset. You must achieve a recovery rate of at least 98%.