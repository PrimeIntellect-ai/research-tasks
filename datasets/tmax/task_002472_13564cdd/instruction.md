You are an administrator tasked with setting up a local user provisioning service. We have a third-party, C-based lightweight HTTP service designed to handle user account provisioning requests, located at `/app/provisioner-1.0`. 

However, this package is currently broken and does not compile or function correctly. Your objective is to fix the package, write an idempotent setup script, and run the service.

Here are the specific requirements:

1. **Fix the Vendored Package:**
   - The package is located in `/app/provisioner-1.0`.
   - Inspect and fix `main.c` and `Makefile`. There is a deliberate bug where the application constructs invalid paths for symlinks and crashes if certain environment variables are missing.
   - The service must compile successfully when `make` is run.

2. **Service Operation:**
   - The compiled service `provisioner` must listen on `127.0.0.1:8080`.
   - The service expects two environment variables: `BASE_DIR` and `WWW_DIR`.
   - When the service receives an HTTP GET request at `/provision?username=<username>&ip=<ip_address>`, it should:
     - Create a directory for the user at `$BASE_DIR/<username>`.
     - Create a directory for the user's web content at `$WWW_DIR/<username>`.
     - Create a symlink named `www` inside `$BASE_DIR/<username>/` that points to `$WWW_DIR/<username>`.
     - Create a file `$BASE_DIR/<username>/route.sh` containing exactly: `ip route add <ip_address> via 10.0.0.1` (this simulates network/routing configuration for the user's dedicated interface).
     - Return an HTTP 200 response with the text `OK`.

3. **Automation Script:**
   - Write a bash script at `/home/user/setup_and_run.sh`.
   - The script must be completely idempotent (running it multiple times should not fail or produce duplicate entries).
   - The script must create the necessary parent directories: `/home/user/managed_users` and `/home/user/public_web`.
   - The script must compile the provisioner (if not already compiled).
   - The script must export `BASE_DIR=/home/user/managed_users` and `WWW_DIR=/home/user/public_web`.
   - The script must start the `provisioner` binary in the background listening on `127.0.0.1:8080`.

Run your `/home/user/setup_and_run.sh` script so the service is actively listening on port 8080 when you finish. Ensure the service stays running.