You are an edge computing engineer configuring an automated deployment and monitoring pipeline for IoT devices. Your task is to set up a local Git-based deployment system that automatically starts a service and runs a health check when new code is pushed.

Please perform the following steps:

1. **Environment Setup**: 
   - Append the following environment variables to `/home/user/.bashrc`:
     - `EDGE_DEVICE_ID=edge-node-42`
     - `EDGE_PORT=8484`

2. **Git Repository Setup**:
   - Initialize a bare Git repository at `/home/user/iot-hub.git`.
   - Create a directory `/home/user/iot-deploy` which will serve as the working directory for the deployed code.

3. **Service Code**:
   - Create a local Git repository at `/home/user/iot-source`.
   - Inside this repository, write a Python script named `edge_service.py`.
   - `edge_service.py` must:
     - Read the `EDGE_PORT` environment variable.
     - Start a simple HTTP server on `127.0.0.1` at the given port.
     - Respond with an HTTP 200 status and the plain text "pong" when the path `/ping` is requested.
     - Run as a background daemon (or detach itself) so it doesn't block the caller, and write its Process ID (PID) to `/home/user/edge_service.pid`.
   - Commit `edge_service.py` to the `master` branch of the `/home/user/iot-source` repository.

4. **Health Monitor**:
   - Create a Python script at `/home/user/health_monitor.py`.
   - The script must:
     - Read `EDGE_DEVICE_ID` and `EDGE_PORT` from the environment.
     - Make an HTTP GET request to `http://127.0.0.1:<EDGE_PORT>/ping` (retry up to 5 times with a 1-second delay if the server is starting).
     - If the response is `pong` with a 200 status code, append the exact line `[<EDGE_DEVICE_ID>] DEPLOYMENT_SUCCESS` to `/home/user/deployment_log.txt`.
     - If it fails after retries, append `[<EDGE_DEVICE_ID>] DEPLOYMENT_FAILED` to the same file.

5. **Git Hook Configuration**:
   - Create a `post-receive` hook in `/home/user/iot-hub.git/hooks/post-receive`.
   - Ensure the hook is executable.
   - The hook must:
     - Source `/home/user/.bashrc` to load the environment variables.
     - Check out the received code into `/home/user/iot-deploy` (e.g., using `git --work-tree=/home/user/iot-deploy --git-dir=/home/user/iot-hub.git checkout -f`).
     - Execute `/home/user/iot-deploy/edge_service.py`.
     - Execute `/home/user/health_monitor.py`.

6. **Trigger Deployment**:
   - Add the bare repository as a remote named `local` to `/home/user/iot-source`.
   - Push the `master` branch to the `local` remote to trigger the deployment pipeline.

Ensure your background service stays running after the hook completes and that the log file is generated correctly.