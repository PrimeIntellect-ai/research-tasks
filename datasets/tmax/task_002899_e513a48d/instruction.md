You are a deployment specialist managing a simulated microservices environment without root access. The current configuration is failing because the services are configured to bind to privileged ports and conflict with each other.

Your task is to fix the configuration and write a robust Python deployment script to automate the rollout of the new version of these services, manage directory symlinks, create backups, and manage the processes.

Here is the initial state of the system you should assume exists:
- Configuration file at `/home/user/services.json`
- Releases directories:
  - `/home/user/releases/service_a_v1/`
  - `/home/user/releases/service_a_v2/`
  - `/home/user/releases/service_b_v1/`
  - `/home/user/releases/service_b_v2/`
- Active deployments (symlinks):
  - `/home/user/deployments/service_a/current` (points to `service_a_v1`)
  - `/home/user/deployments/service_b/current` (points to `service_b_v1`)
- Empty directories for backups and process pids:
  - `/home/user/backups/`
  - `/home/user/run/`

Perform the following steps:
1. Fix the network misconfiguration in `/home/user/services.json`. Change `service_a` to bind to host `127.0.0.1` on port `9001`, and `service_b` to bind to host `127.0.0.1` on port `9002`.
2. Write a Python script at `/home/user/deploy.py` that implements the following deployment logic:
   - Read the corrected `/home/user/services.json`.
   - Iterate through each service. For each service:
     - Create a compressed tarball backup of the directory currently pointed to by the `current` symlink. Save it exactly as `/home/user/backups/<service_name>_backup.tar.gz`.
     - Update the symlink at `/home/user/deployments/<service_name>/current` to point to the new release directory (`/home/user/releases/<service_name>_v2`).
     - Start a Python HTTP server in the background for that service using the command: `python3 -m http.server <port> --bind <host> --directory /home/user/deployments/<service_name>/current`
     - Save the PID of the newly spawned background process into a text file at `/home/user/run/<service_name>.pid`.
3. Execute your `/home/user/deploy.py` script so that both services are successfully deployed, backed up, and running in the background.

Ensure your script handles paths correctly and leaves the HTTP servers running when it exits.