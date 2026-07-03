You are tasked with fixing and deploying a local diagnostic web service that is currently failing to start. The service is located in `/home/user/service/`.

Currently, if you try to run the service, it silently fails and exits, preventing any connections. You need to diagnose the environment, fix the storage and link configuration, implement a basic supervisor, and verify connectivity.

Please perform the following steps:

1. **Fix the Configuration Link**: The service expects a configuration symlink at `/home/user/service/config.json`. Currently, it points to a revoked configuration. Re-link it to point to the valid configuration file located at `/home/user/service/configs/production.json`.
2. **Fix the Storage Constraint**: The service requires a cache directory to function, but it is missing, simulating a storage allocation failure. Create the directory `/home/user/service/cache/`.
3. **Implement Process Supervision**: Create a bash script at `/home/user/service/supervisor.sh`. This script must:
   - Run in an infinite `while` loop.
   - Execute `python3 /home/user/service/daemon.py` inside the loop.
   - If the daemon crashes or exits, the loop should automatically restart it.
   - Start your `supervisor.sh` script in the background (e.g., using `nohup bash /home/user/service/supervisor.sh &`) so the service stays running.
4. **Verify Connectivity**: Once the service is running, it will listen on `127.0.0.1:8181`. Use `curl` to make a GET request to `http://127.0.0.1:8181/health`. Save the exact response output to `/home/user/service/health_check.txt`.

Ensure your supervisor is running in the background and the `health_check.txt` file is populated correctly before completing the task.