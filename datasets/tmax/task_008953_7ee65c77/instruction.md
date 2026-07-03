You are a Linux Systems Engineer tasked with building a local CI/CD deployment script to harden an application's configuration and manage its lifecycle.

There is an application archive located at `/home/user/source.tar.gz`. You need to automate its extraction, configuration hardening, and startup.

Write a Python script at `/home/user/deploy.py` that performs the following steps in order:
1. Extracts the archive `/home/user/source.tar.gz` into the directory `/home/user/app` (create the directory if it does not exist).
2. Hardens the filesystem permissions for the extracted files:
   - All files directly inside `/home/user/app/bin/` must have exact `0500` permissions (read and execute by owner only).
   - All files directly inside `/home/user/app/config/` must have exact `0400` permissions (read by owner only).
3. Modifies the configuration file `/home/user/app/config/worker.ini` to fix a missing dependency and bind to the correct network port:
   - Append the line `After=network.target` to the end of the `[Unit]` section.
   - Change the line starting with `Port=` in the `[Service]` section to `Port=9090`.
   - Note: Modifying the file might require temporarily changing its permissions and restoring them back to `0400` afterward.
4. Spawns the application server `/home/user/app/bin/server.py` as a background process (detached or running asynchronously via `subprocess`) so that the deployment script can exit while the server keeps running.
5. Writes a deployment log to `/home/user/deploy.log` containing exactly these four lines (replace `<pid>` with the actual integer Process ID of the spawned server):
   [SUCCESS] Extracted files
   [SUCCESS] Permissions hardened
   [SUCCESS] Config updated
   [SUCCESS] Service running on PID <pid>

Once you have written `/home/user/deploy.py`, execute it to complete the deployment. Leave the background server running.