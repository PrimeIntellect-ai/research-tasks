You are an edge computing engineer responsible for deploying updates to remote IoT devices. Since these devices have limited resources and legacy interactive administrative interfaces, your deployment automation must handle system checks, connectivity diagnostics, and interactive prompts.

Your task is to write a Python script `/home/user/edge_manager.py` that automates a deployment process on the local system (simulating an edge device). 

Before writing and running your script, ensure the mock edge service is running in the background. You can start it by running:
`python3 /home/user/mock_service.py &`

Your Python script (`/home/user/edge_manager.py`) must perform the following actions sequentially:

1. **Storage Monitoring**: 
   Check the available disk space for the directory `/home/user/device_data` (create this directory if it doesn't exist). 
   - If available space is less than 5MB, write `STORAGE: FAILED` to `/home/user/edge_status.log` and exit.
   - If sufficient, write `STORAGE: OK` to `/home/user/edge_status.log` and continue.

2. **Connectivity Diagnostics**:
   Test if the mock registry service is reachable by attempting a TCP connection to `127.0.0.1` on port `9090`.
   - If the connection fails, append `CONNECTIVITY: FAILED` to `/home/user/edge_status.log` and exit.
   - If the connection succeeds, append `CONNECTIVITY: OK` to `/home/user/edge_status.log` and continue.

3. **Interactive Container Management (Expect Scripting)**:
   The legacy edge daemon is controlled via an interactive script located at `/home/user/interactive_cli.py`. You must use the Python `pexpect` module to interact with it programmatically.
   When run, `/home/user/interactive_cli.py` will prompt you with the following:
   - `Enter Edge ID: ` -> You must supply: `EDGE-999`
   - `Enter Passcode: ` -> You must supply: `314159`
   - `edge-shell> ` -> First, you must stop the legacy container by sending: `stop legacy-sensor`
   - `edge-shell> ` -> Next, you must start the new container by sending: `start vision-sensor-v2`
   - `edge-shell> ` -> Finally, exit the shell by sending: `exit`

4. **Final Logging**:
   After the `pexpect` sequence completes successfully, append `DEPLOYMENT: SUCCESS` to `/home/user/edge_status.log`.

Run your script to complete the deployment. An automated test will verify the contents of `/home/user/edge_status.log` and the internal state of the interactive CLI (saved to `/home/user/cli_backend.log`).