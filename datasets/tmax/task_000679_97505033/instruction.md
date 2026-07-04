You are a support engineer tasked with investigating a critical incident. A customer reported that their automated diagnostics tool is receiving intermittent HTTP 500 Internal Server Errors when querying our Log Diagnostics API. They provided the exact JSON payload that triggers the issue, which is saved at `/home/user/customer_payload.json`.

The system consists of three services:
1. A Redis cache
2. A backend Data Service (mocked)
3. The Flask API (which has the bug)

Your objectives are:
1. **Service Integration:** Start the multi-service environment. There is a startup script at `/app/services/start_all.sh` which launches Redis (port 6379) and the Data Service (port 9000). The Flask API source code is located in a local Git repository at `/app/api_repo`. You need to start the Flask API so it listens on `127.0.0.1:8000`.
2. **Delta Debugging:** The `customer_payload.json` is massive. Systematically minimize this JSON payload to find the absolute minimal set of keys/values that still triggers the HTTP 500 error on the `POST /query` endpoint. Save this minimal valid JSON to `/home/user/minimal_payload.json`.
3. **Log & Traceback Analysis:** Analyze the API logs to find the Python traceback caused by the minimal payload. 
4. **Regression Finding:** The `api_repo` is a Git repository. The `main` branch HEAD is currently failing. A known good tag `v1.0` exists. Use `git bisect` (or a similar manual approach) to identify the exact commit hash that introduced the bug. Write this full commit hash to `/home/user/bad_commit.txt`.
5. **Fix the Code:** Patch the bug in `/app/api_repo/app.py` so that the API correctly handles the minimal payload without crashing, and returns a 200 OK.
6. **Final State:** Ensure all services are running and the patched Flask API is actively listening on `127.0.0.1:8000`. The automated verifier will send HTTP protocol requests to this port to ensure the regression is fixed and upstream services are correctly integrated.

Do not change the API endpoints or the expected upstream service ports.