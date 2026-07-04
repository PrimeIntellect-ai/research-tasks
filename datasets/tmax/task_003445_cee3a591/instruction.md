We need you to implement a lightweight, Git-driven Kubernetes operator simulation. You will be configuring a Git repository, writing a C-based Git hook, reverse-engineering a provided configuration parser, and writing a C-based HTTP server to expose the resulting manifests.

Here are your detailed instructions:

1. **Git Repository & Directory Structure Setup:**
   - Create a bare Git repository at `/home/user/operator.git`.
   - Create a staging directory at `/home/user/staging`.
   - Create a web root directory at `/home/user/webroot`.
   - Ensure you have a standard directory structure for these folders.

2. **Reverse Engineer the CRD Parser:**
   - We have provided a stripped, compiled binary at `/app/crd_parser`. 
   - This binary parses our custom manifest format into valid Kubernetes JSON, but its usage is undocumented and it requires a specific secret key to run correctly.
   - Investigate `/app/crd_parser` (using tools like `strings`, `ltrace`, or `objdump`) to discover its command-line arguments and the hardcoded secret key.

3. **C-Based Git Hook (post-receive):**
   - Write a C program and compile it to `/home/user/operator.git/hooks/post-receive`. Ensure it has execute permissions.
   - When a git push is received, your hook must:
     a) Extract the incoming files into `/home/user/staging`.
     b) Locate the file named `deployment.crd` in the staging area.
     c) Execute `/app/crd_parser` on `deployment.crd` using the secret key you discovered, and redirect the JSON output to `/home/user/webroot/deployment.json`.
     d) Set the file permissions of `/home/user/webroot/deployment.json` strictly to `0600` (read/write by owner only).
     e) Create or update a symlink at `/home/user/webroot/latest.json` pointing to `/home/user/webroot/deployment.json`.

4. **C-Based Operator HTTP Server:**
   - Write an HTTP server in C (`/home/user/server.c`) and compile it to `/home/user/server`.
   - The server must run as a daemon (or in the background) and listen on `127.0.0.1:8080`.
   - It must implement a single endpoint: `GET /api/v1/manifest`.
   - When this endpoint is requested, the server must read the file at `/home/user/webroot/latest.json` and return its contents with an HTTP 200 OK status and `Content-Type: application/json`.

5. **Scheduled Health Check (Cron):**
   - Write a shell script at `/home/user/health.sh` that uses `curl` to fetch `http://127.0.0.1:8080/api/v1/manifest` and appends the HTTP status code to `/home/user/health.log`.
   - Configure a user-level crontab to execute `/home/user/health.sh` every minute.

Ensure your HTTP server is running and the `operator.git` repository is ready to accept pushes by the end of your run.