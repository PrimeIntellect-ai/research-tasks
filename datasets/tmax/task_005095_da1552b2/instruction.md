You are tasked with building a local, Bash-driven GitOps deployment system to serve a transcription API. Your setup must automatically back up configurations, deploy new commits, and supervise the running processes. 

A provided audio file is located at `/app/transmission.wav`. There is also a local utility at `/opt/transcribe.sh` that takes an audio file path as an argument and outputs its text transcription.

Follow these instructions precisely to set up the system:

1. **Git Server and Backup Hook:**
   - Create a bare Git repository at `/home/user/config.git`.
   - Create directories `/home/user/active_configs/`, `/home/user/backups/`, and `/home/user/workspace/`.
   - Write a `post-receive` Git hook for `config.git`. Upon receiving a push, the hook must:
     a) Compress the current contents of `/home/user/active_configs/` into a tarball at `/home/user/backups/config-<UNIX_TIMESTAMP>.tar.gz`.
     b) Extract the newly pushed tree into `/home/user/active_configs/`.
     c) Touch a file `/home/user/active_configs/.reload` to signal the supervisor.

2. **Process Supervision (`/home/user/supervisor.sh`):**
   - Write a Bash script that acts as a process supervisor. 
   - It should launch two background services: `nginx` (using `/home/user/active_configs/nginx.conf`) and the backend application (`/home/user/active_configs/backend.sh`).
   - The supervisor must monitor these processes. If either crashes or exits, it must restart them immediately.
   - The supervisor should also poll for the existence of `/home/user/active_configs/.reload` (created by the Git hook). If found, it should remove the `.reload` file, gracefully terminate the current Nginx and backend processes, and spawn the new versions.

3. **Application Manifests & The Bug Fix:**
   - In `/home/user/workspace/`, you must create the initial code and configurations. Initialize this directory as a Git repo and link it to your bare repo.
   - **Nginx Config (`nginx.conf`):** Create an Nginx configuration that listens on `127.0.0.1:8080` (HTTP). Ensure it runs entirely in user-space (store pid and temp paths in `/home/user/active_configs/`). It should proxy all requests for `location /transcribe` to a Unix socket using `proxy_pass http://unix:/home/user/active_configs/backend.sock:;`.
   - **Backend (`backend.sh`):** Write a Bash-based HTTP server (you may use `socat` or `nc`) that listens on the Unix socket `/home/user/active_configs/backend.sock`. 
   - *Current Bug Scenario:* Imagine the previous team left a mismatch. Ensure your Nginx config and your backend script exactly agree on the socket path `/home/user/active_configs/backend.sock`.
   - When the backend receives an HTTP GET request on `/transcribe`, it must execute `/opt/transcribe.sh /app/transmission.wav` and return a valid `HTTP/1.0 200 OK` response with `Content-Type: text/plain` and the resulting transcript as the body.

4. **Integration:**
   - Commit `nginx.conf` and `backend.sh` in your workspace and push them to `config.git`.
   - Start your `supervisor.sh` in the background.

The automated verifier will make an HTTP GET request to `http://127.0.0.1:8080/transcribe` and expects the exact transcribed text. Ensure your supervisor and deployed services are running.