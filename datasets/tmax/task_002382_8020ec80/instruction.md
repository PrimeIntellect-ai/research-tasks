You are an edge computing engineer deploying a diagnostic automation script for local IoT gateways. 

Your task is to create and run a Python script at `/home/user/edge_monitor.py` that manages a container instance, checks its network connectivity, and securely logs the results with automatic log rotation.

Write the Python script to meet the following requirements:
1. **Container Lifecycle Management**: Use Python's `subprocess` module to start an Apptainer instance named `iot_worker` using the `docker://alpine:latest` image. (Command: `apptainer instance start docker://alpine:latest iot_worker`).
2. **Directory & Log Configuration**: Ensure the directory `/home/user/edge_logs` exists (create it if not). Configure a Python logger using `logging.handlers.RotatingFileHandler` to write to `/home/user/edge_logs/status.log`. The handler must be configured with `maxBytes=40` and `backupCount=3`. The log format should just be the raw message (e.g., `%(message)s`).
3. **Connectivity Diagnostics**: Create a loop that iterates exactly 8 times. In each iteration:
   - Use `subprocess` to execute a ping command inside the running Apptainer instance: `apptainer exec instance://iot_worker ping -c 1 127.0.0.1`
   - If the ping command succeeds (exit code 0), write the exact string `"Ping successful"` to the logger.
   - If it fails, write `"Ping failed"` to the logger.
4. **Cleanup**: After the loop finishes, stop the container instance using `apptainer instance stop iot_worker`.

Finally, execute your script using `python3 /home/user/edge_monitor.py` so that the logs are generated and the container is started and stopped.

Ensure your script handles standard errors gracefully, but wait for the commands to finish (synchronously).