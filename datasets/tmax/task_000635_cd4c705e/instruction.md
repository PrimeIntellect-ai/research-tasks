You are an infrastructure engineer tasked with automating the provisioning of our internal data processing stack. 

Currently, our multi-service stack (consisting of an Auth API, a Redis broker, and a Worker daemon) is brought up using a slow, brittle shell script (`/app/slow_provision.sh`) that relies on arbitrary `sleep` commands to wait for service readiness. This causes provisioning to take far too long and occasionally fail if a service takes longer than the fixed sleep time.

Your objective is to write a robust, highly optimized Python provisioning script located at `/home/user/fast_provision.py`.

Requirements:
1. **Container / Service Lifecycle:** The services are started via the existing wrapper script `/app/start_services.sh`. Your Python script should execute this wrapper to launch the background services.
2. **Connectivity Diagnostics:** Instead of hardcoded sleeps, your Python script must actively poll the services to detect exactly when they are ready. 
   - Redis runs on `localhost:6379`.
   - The Auth API runs on `localhost:8080`.
   - The Worker exposes a healthcheck file socket at `/tmp/worker_health.sock`.
3. **Expect Scripting / Interactive Automation:** Once all three services are responsive, your script must execute a CLI tool `/app/admin_cli.py init-cluster` which asks interactive prompts ("Enter admin username:", "Enter admin password:", "Confirm [y/N]:"). Use Python's `pexpect` module to automate this interactive configuration (Username: `admin`, Password: `supersecret`, Confirm: `y`).
4. **Scheduled Task Configuration:** After successful provisioning, create a user-level cron job that runs `/app/health_check.py` every 5 minutes to continuously monitor the stack.

The final execution time of `/home/user/fast_provision.py` must be significantly faster than the reference `/app/slow_provision.sh`. We will run your script and calculate the speedup metric.

Ensure your script is executable (`chmod +x /home/user/fast_provision.py`) and cleanly exits with code 0 upon successful provisioning. Write a log file to `/home/user/provision.log` containing the exact output of the `admin_cli.py` execution.