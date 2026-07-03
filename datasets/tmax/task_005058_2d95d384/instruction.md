You are an engineer tasked with diagnosing and fixing a multi-language microservice application that currently fails to start due to severe filesystem configuration issues. The application's main startup script is failing, and the deployment pipeline is blocked.

Your objectives are to fix the filesystem structure, write a verification script (simulating a CI/CD pipeline step), and implement a missing Node.js reverse proxy to restore the system.

Here are your specific requirements:

1. **Fix the Filesystem Structure:**
   The application resides in `/home/user/app`. Inside this directory, there are two broken symlinks:
   - `/home/user/app/conf` currently points to a forbidden system directory. Remove this broken symlink and recreate it so that it points to `/home/user/app/internal_conf`. (You will need to create the target directory).
   - `/home/user/app/logs` currently points to another forbidden directory. Remove it and recreate it to point to `/home/user/app/local_logs`. (Create the target directory).

2. **Configuration File:**
   Create a JSON configuration file at `/home/user/app/conf/backends.json` (which will actually write to the `internal_conf` directory due to the symlink). The file must contain exactly this JSON array representing backend addresses:
   `["http://127.0.0.1:8081", "http://127.0.0.1:8082"]`

3. **CI/CD Verification Script:**
   Write a robust bash script at `/home/user/ci_cd_verify.sh` to act as a pre-deployment check. The script must:
   - Use strict error handling (`set -e`).
   - Check if `/home/user/app/conf` and `/home/user/app/logs` are valid, resolvable directories (not broken symlinks).
   - Check if `/home/user/app/conf/backends.json` exists and is readable.
   - If all checks pass, write the exact string `PIPELINE_SUCCESS` to `/home/user/deploy_status.txt` and exit with code 0.
   - If any check fails, write `PIPELINE_FAILED` to `/home/user/deploy_status.txt` and exit with code 1.
   Make sure the script is executable.

4. **Node.js Reverse Proxy:**
   Write a Node.js script at `/home/user/app/proxy.js`. This script should:
   - Read the `/home/user/app/conf/backends.json` file to get the list of backend URLs.
   - Start an HTTP server listening on `127.0.0.1` port `8080`.
   - When a request is received, it should simply return a `200 OK` response with the text `PROXY_ACTIVE` (do not actually proxy the request to the backends for this task, just simulate the listener setup and configuration loading).
   - Ensure the script writes its process ID (PID) to `/home/user/app/logs/proxy.pid` upon successfully starting the server.

You do not need to start the proxy manually, but you must ensure that all files, symlinks, and scripts are perfectly configured so that an automated test can start `proxy.js` and execute `ci_cd_verify.sh`.