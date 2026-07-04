You are a FinOps analyst tasked with automating the archiving of expensive cloud logs. You need to construct a robust, idempotent bash script that acts as a local CI/CD deployment step to analyze log sizes, query a metadata API, and archive the files accordingly.

The system setup simulates a missing service dependency (similar to a missing `After=` systemd directive). A metadata API exists but takes a few seconds to boot, and it only binds to an internal port. 

Write a bash script at `/home/user/run_pipeline.sh` that performs the following exact workflow:

1. **Idempotent Setup:** Ensure the directories `/home/user/archive` and `/home/user/reports` exist.
2. **Service & Tunnel Initialization:**
   - Execute the provided python API server located at `/home/user/api/server.py` in the background. This server binds to port `9090`.
   - Create a local port forward (simulating an SSH tunnel) using `socat` or `nc` to forward local port `8080` to `localhost:9090` in the background.
3. **Robust Synchronization:** 
   - Implement a polling mechanism in your script to wait until `http://localhost:8080/health` returns an HTTP 200 OK status. Do not proceed until the tunnel and API are fully responsive.
4. **Filesystem Processing:**
   - Scan the directory `/home/user/logs_pool/` for all `.log` files.
   - For each file, query the API at `http://localhost:8080/tier/<filename>`. The API returns a JSON response like `{"tier": "archive"}` or `{"tier": "retain"}`.
   - If the tier is `"archive"`, compress the file using `gzip` and move the resulting `.gz` file to `/home/user/archive/`. 
   - Ensure the script is idempotent; if run twice, it should not fail or corrupt already archived files.
5. **Reporting:**
   - Calculate the total original size in bytes of the files that were archived during the run.
   - Write a JSON report to `/home/user/reports/summary.json` with the exact following structure:
     ```json
     {
       "archived_count": 2,
       "freed_bytes": 1234567
     }
     ```
   - (Where 2 and 1234567 are replaced with the actual count and total original bytes of the archived files).

Make sure the script is executable (`chmod +x`). Once you have written the script, execute it so the final state (the archive directory and the summary JSON) is generated.