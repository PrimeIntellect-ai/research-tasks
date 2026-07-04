You are managing a local simulated microservice environment. We have a health-check script that runs periodically to gather metrics from a local backend, but it's currently failing due to environment, path, and networking configuration mismatches. 

Your goal is to fix the setup so the checker script runs successfully, regardless of the current working directory.

Here is the current state of the system:
1. There is a backend service running locally on port `8080`.
2. There is a checker script located at `/home/user/service/checker.py`.
3. The checker script expects to load its configuration from `config.json`.
4. The checker script attempts to connect to the backend via `localhost:9999` (simulating a legacy hardcoded port).
5. The checker script writes its output to `/home/user/service/logs/result.json`. `/home/user/service/logs` is currently a broken symlink pointing to `/home/user/data/logs/`.

Perform the following tasks:
1. **Fix the Directory Structure**: Ensure the target directory for the log symlink exists so the script can write to `/home/user/service/logs/result.json`.
2. **Setup Port Forwarding**: The checker script hardcodes port `9999`, but the backend runs on port `8080`. Set up a persistent local port forward (e.g., using `socat` or a background Python process) so that traffic to `127.0.0.1:9999` is transparently forwarded to `127.0.0.1:8080`.
3. **Fix the Code (Path Issue)**: Edit `/home/user/service/checker.py`. The script currently tries to open `config.json` using a relative path. Update it to use the absolute path (`/home/user/service/config.json`) so it won't fail if executed from a different directory (like it does when run via cron).
4. **Execute**: Once fixed, run the script from the home directory: `cd /home/user && python3 /home/user/service/checker.py`.

You are successful if the script runs without errors and successfully creates `/home/user/data/logs/result.json` containing the backend's response data.