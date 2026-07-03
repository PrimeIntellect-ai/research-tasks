You are an infrastructure engineer automating the provisioning of a dual-protocol telemetry relay. 

We have received an automated telemetry provisioning package. Part of the security requirement is that the provisioning PIN is delivered out-of-band as an audio file containing DTMF (Dual-Tone Multi-Frequency) tones. 

Your tasks are to:

1. **Extract the PIN from Audio:**
   An audio file is located at `/app/telemetry.wav`. It contains a sequence of DTMF tones representing a numeric PIN. Analyze this file (you may write a Python script or use tools like `multimon-ng` which you can install locally) to extract the PIN. 

2. **Directory and Link Management:**
   Create the following directory structure in your home directory (`/home/user`):
   - `/home/user/telemetry_app/releases/v1`
   - `/home/user/telemetry_app/logs`
   
   Create a symlink at `/home/user/telemetry_app/current` that points to `/home/user/telemetry_app/releases/v1`.
   Inside `/home/user/telemetry_app/releases/v1`, create a file named `status.json` with the exact content: `{"status": "provisioned"}`

3. **Multi-Protocol Telemetry Service:**
   Write a single Python script at `/home/user/telemetry_app/server.py` that simultaneously runs two services (you can use `threading` or `asyncio`):
   - **HTTP Service:** Listens on `127.0.0.1:9080` and serves static files from the `/home/user/telemetry_app/current` directory.
   - **TCP Auth Service:** Listens on `127.0.0.1:9081`. When a raw TCP client connects, it must wait for the client to send a line of text. If the text exactly matches the extracted DTMF PIN (ignoring leading/trailing whitespace), the server must respond with `AUTH_OK\n` and close the connection. If it does not match, respond with `AUTH_FAIL\n` and close the connection.

   Run this Python server in the background so it is active.

4. **Expect Scripting for Health Checks:**
   Write an `expect` script at `/home/user/telemetry_app/health_check.exp`. This script must:
   - Spawn a connection to the TCP Auth Service (`nc 127.0.0.1 9081`).
   - Send the extracted PIN.
   - Expect the string `AUTH_OK`.
   - Exit with status `0` if successful, or `1` if it times out or fails.

5. **Scheduled Task Configuration:**
   Install a user crontab that runs the `health_check.exp` script every 5 minutes. The cron job should redirect standard output and standard error to `/home/user/telemetry_app/logs/health.log`.

Ensure your Python server is running in the background and the crontab is installed before you finish.