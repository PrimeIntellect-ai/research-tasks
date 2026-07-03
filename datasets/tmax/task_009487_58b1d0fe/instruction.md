You are tasked with building a user-space mock Kubernetes Operator in Python and managing its lifecycle via a custom init script. Because you do not have root access, this operator will simulate network routing changes by generating a configuration file rather than modifying the actual host networking.

Your objective is to complete the following phases:

**Phase 1: Directory Setup**
Create the following directory structure in `/home/user`:
- `/home/user/k8s-manifests/` (The watch directory)
- `/home/user/active-manifests/` (The symlink directory)
- `/home/user/network/` (The output directory for network configs)

**Phase 2: The Operator Logic (Python)**
Write a Python script at `/home/user/operator.py` that acts as a continuous daemon (checking every 1 second). The script must do the following on each iteration:
1. Scan `/home/user/k8s-manifests/` for files ending in `.yaml`.
2. For each YAML file, parse it (you may use basic string parsing or the `yaml` module if you install it). Expect the format to have `kind: Route`, `metadata:\n  name: <name>`, and `spec:\n  routeIP: <ip>`.
3. If it is a `Route` kind:
   - Create a symlink in `/home/user/active-manifests/<name>.yaml` pointing to the original manifest in `k8s-manifests`. Only create it if it doesn't already exist.
   - Append a routing rule to `/home/user/network/routes.conf`. The rule must exactly match this format: `ip route add <ip> dev mock0 metric 100` (ensure no duplicate lines are written for the same manifest across iterations).

**Phase 3: Service Lifecycle Management**
Write a bash init script at `/home/user/operator.sh` that implements `start`, `stop`, and `status` commands to manage `operator.py` as a background daemon.
- `start`: Runs the python script in the background. Writes its PID to `/home/user/operator.pid`.
- `stop`: Reads `/home/user/operator.pid`, kills the process, and removes the PID file.
- `status`: Checks if the process listed in `/home/user/operator.pid` is running. Exits 0 if running, 1 if not.
Make sure the script is executable.

**Phase 4: Execution and Manifest Creation**
1. Start the operator daemon using your init script: `/home/user/operator.sh start`.
2. Create two mock manifest files in `/home/user/k8s-manifests/`:
   - `route-alpha.yaml`: Name should be `alpha-route`, routeIP should be `192.168.10.0/24`.
   - `route-beta.yaml`: Name should be `beta-route`, routeIP should be `10.5.0.0/16`.
3. Wait at least 2 seconds for the operator to process the files.
4. Stop the operator daemon using your init script: `/home/user/operator.sh stop`.

When finished, ensure `routes.conf` has been generated with the correct entries, the symlinks exist, and the daemon is cleanly stopped.