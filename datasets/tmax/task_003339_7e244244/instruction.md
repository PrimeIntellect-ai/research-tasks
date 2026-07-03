I need you to organize a sprawling directory of legacy project logs and build a Rust-based API to manage them securely. 

Currently, our application spits out disorganized logs into nested folders under `/home/user/raw_logs/`. We have a proprietary legacy tool at `/app/legacy_verifier` (a stripped binary) that checks if a log file meets our strict compliance format (it acts as a black-box oracle; if a file is compliant, it exits with code 0, otherwise it exits with a non-zero code).

Here is your multi-step task:

1. **Log Cleanup & Traversal:**
   Recursively traverse `/home/user/raw_logs/`. You will find many `.log` files. 
   These are multi-line log files where each entry starts with a timestamp bracket. Some of these log files have incorrectly formatted timestamps in the format `[DD-MM-YYYY HH:MM:SS]`. 
   You must perform a large-scale text edit to standardize all bracketed timestamps to `[YYYY-MM-DD HH:MM:SS]`. Keep multi-line stack traces intact.

2. **Compliance Filtering:**
   After standardizing timestamps, run `/app/legacy_verifier <filepath>` on every log file. 
   Discard (delete) any files that fail validation. 

3. **Log Reorganization:**
   Move all compliant log files into `/home/user/clean_logs/YYYY-MM-DD/` directories, where `YYYY-MM-DD` corresponds to the date of the *first* log entry in that file.

4. **Rust API Development:**
   Create a Rust HTTP web server in `/home/user/log_api/`. You may use `axum`, `warp`, or `actix-web`.
   The server MUST listen on exactly `127.0.0.1:8080`.
   The server must require an `Authorization: Bearer project-alpha-99` header for all requests. Return `401 Unauthorized` otherwise.
   
   Implement the following endpoints:
   - `GET /download?date=YYYY-MM-DD`
     This endpoint must dynamically package the contents of `/home/user/clean_logs/<date>/` into a standard `tar.gz` archive and return it as a binary stream (content-type: `application/gzip`). If the date directory does not exist, return a `404 Not Found`.
   - `POST /verify`
     Accepts a JSON payload: `{"path": "/absolute/path/to/file"}`. It must execute `/app/legacy_verifier` against the provided path. Return `{"status": "compliant"}` if it exits 0, and `{"status": "invalid"}` otherwise.

Build and start the Rust server in the background so it is actively listening on `127.0.0.1:8080` when you complete the task.