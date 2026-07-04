You are tasked with fixing and extending a custom Python-based "operator" that mimics a Kubernetes controller by managing local user-space processes. 

Currently, the script `/home/user/operator.py` reads JSON service manifests from `/home/user/manifests/` and generates a bash script `/home/user/launcher.sh` to start them. However, it is fundamentally broken: it fails to respect start-order dependencies (similar to systemd's `After=` missing), lacks storage quota monitoring, and is missing a required webhook service.

Here are your objectives:

1. **Implement Dependency Ordering in `operator.py`:**
   Modify `/home/user/operator.py`. The script currently reads all `.json` files in `/home/user/manifests/`. Each manifest has a `name`, `command`, and an optional `depends_on` (a list of service names that must start before this one). 
   You must update `operator.py` so that it generates `/home/user/launcher.sh` with the commands ordered according to their dependencies (a topological sort). If there is a circular dependency, the script should exit with code 1 and write "CIRCULAR_DEPENDENCY" to `/home/user/operator.log`.
   
   The generated `/home/user/launcher.sh` must:
   - Begin with `#!/bin/bash`
   - Echo the name of each service being started to `/home/user/start_order.txt` (e.g., `echo "Starting db" >> /home/user/start_order.txt`) immediately before executing its command.
   - Execute the `command` specified in the manifest in the background (append `&`).
   - Sleep for 1 second after starting each service.

2. **Implement Storage Monitoring in `operator.py`:**
   Before processing any manifests, the operator must calculate the total size (in bytes) of all files in `/home/user/data/` (including subdirectories). If the total size strictly exceeds `1024000` bytes (1000 KB), `operator.py` must:
   - Write exactly "STORAGE_QUOTA_EXCEEDED" to `/home/user/operator.log`.
   - Immediately exit with code 2 without generating the launcher script.

3. **Create a Webhook Manifest:**
   Create a new manifest at `/home/user/manifests/webhook.json`. It must contain a JSON object with:
   - `"name"`: `"webhook"`
   - `"command"`: `"python3 -m http.server 8080 --directory /home/user/public"`
   - `"depends_on"`: `["backend"]`

4. **Execution:**
   - Ensure `/home/user/operator.py` is executable (`chmod +x`).
   - Run `/home/user/operator.py`.
   - Run the generated `/home/user/launcher.sh`.

At the end of your task, `/home/user/start_order.txt` should exist and contain the ordered sequence of started services. Do not start the services on ports that require root (port 8080 is fine). You may use standard Python libraries only.