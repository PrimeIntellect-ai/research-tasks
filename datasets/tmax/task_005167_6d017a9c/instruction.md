We have a local configuration management pipeline built in Bash that is supposed to interpolate environment variables into a JSON configuration template, track changes, and serve the final configuration via a lightweight HTTP API. However, the system is currently broken.

You need to fix the vendored package handling the web serving and interpolation, and then orchestrate the pipeline.

Here are your objectives:

1. **Fix the Vendored Package:**
   There is a custom vendored bash package located at `/app/bash-serve-config/`. It contains two main scripts:
   - `interpolate.sh`: A script that replaces mustache-style template variables (e.g., `{{ DB_HOST }}`) in a text stream using `sed` or `awk`. Currently, the regex in this script is broken—it uses a greedy match that destroys lines with multiple variables, or fails to parse variable names correctly. Fix it so it accurately interpolates variables sourced from a given `.env` file.
   - `server.sh`: A lightweight HTTP server using `socat`. It is supposed to listen on the port specified by the `PORT` environment variable, but it has a bug where it ignores the environment variable or binds to the wrong port. Fix it so it properly binds to `127.0.0.1` on the port specified by `$PORT` (defaulting to 8080 if not set).

2. **Create the Orchestrator DAG:**
   Write a master script at `/home/user/orchestrator.sh` (make it executable). This script must act as a simple DAG orchestrator that executes the following steps in order, logging its progress:
   - **Step 1 (Setup):** Source variables from `/home/user/vars.env`.
   - **Step 2 (Interpolation & Imputation):** Use `/app/bash-serve-config/interpolate.sh` to read `/home/user/config.template.json` and generate `/home/user/config.json`. If a variable is missing from `vars.env`, impute a default value of `"UNKNOWN"`.
   - **Step 3 (Logging):** Append a timestamped log entry to `/home/user/pipeline.log` in the exact format: `[YYYY-MM-DD HH:MM:SS] Pipeline run complete. Config generated.`
   - **Step 4 (Service Restart):** Kill any currently running instance of `server.sh`, then start `/app/bash-serve-config/server.sh` in the background serving `/home/user/config.json` on port `8080`.

3. **Start the Service:**
   Once your script is ready, run `/home/user/orchestrator.sh` so the HTTP server is running and listening on `127.0.0.1:8080`.

The automated verifier will update `/home/user/vars.env`, re-run your `orchestrator.sh`, and make HTTP GET requests to `127.0.0.1:8080` to verify the JSON structure and correct interpolation of multiple variables on single lines. Ensure your HTTP server responds with standard HTTP headers (e.g., `HTTP/1.1 200 OK`) and the file content.