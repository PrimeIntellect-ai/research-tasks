You are an infrastructure engineer automating the provisioning of a secure authentication gateway. We have received a secure audio transmission containing an essential passcode that must be used to secure our new multi-protocol service.

Perform the following tasks to stand up the service:

1. **Audio Passcode Extraction**:
   There is an audio file at `/app/urgent_comms.wav`. Analyze it (e.g., using Python speech recognition libraries or tools like whisper/ffmpeg) to extract the spoken passcode. Convert the spoken word(s) to a single uppercase alphanumeric string with no spaces (e.g., if the audio says "bravo niner", the passcode is "BRAVONINER").

2. **Idempotent Provisioning Script**:
   Create a Python script at `/home/user/provision.py` that, when executed, idempotently performs the following environment setup:
   - Creates a directory `/home/user/app_logs/` with strict permissions (0700).
   - Creates an empty log file at `/home/user/app_logs/auth.log` with permissions 0600.
   - Generates an SSH keypair for the `user` and authorizes it in `/home/user/.ssh/authorized_keys` so that `ssh localhost` works without a password prompt or strict host key checking.
   - Creates a valid logrotate configuration file at `/home/user/logrotate.conf` that rotates `/home/user/app_logs/auth.log` daily, keeps 5 backups, compresses them, and creates a new file with 0600 permissions.

3. **Multi-Protocol Authentication Service**:
   Develop a Python service script at `/home/user/auth_server.py` that implements a dual-protocol server using standard library modules (e.g., `http.server` and `socketserver`). Run it as a background daemon.
   - **HTTP Component**: Must listen on `127.0.0.1:8888`. It must accept `GET` requests. If the request includes the header `X-Auth-Passcode` with the exact extracted passcode, it must return a 200 OK status with the exact text `ACCESS_GRANTED`. Otherwise, it must return 403 Forbidden.
   - **TCP Component**: Must listen on raw TCP port `127.0.0.1:8889`. It must accept incoming connections, read exactly one line of text (up to `\n`). If the text matches the passcode, it must respond with `ACCESS_GRANTED\n` and close the connection. Otherwise, it responds with `DENIED\n` and closes.
   - **Logging**: Both components must append a line to `/home/user/app_logs/auth.log` for every attempt. The line must be formatted exactly as: `[PROTOCOL] STATUS` (e.g., `[HTTP] 200` or `[TCP] DENIED`).

4. **Port Forwarding**:
   Establish a persistent SSH local port forward running in the background. It must forward local port `9999` to `127.0.0.1:8888` on localhost.

Run your provisioning script, start your server, and establish the SSH tunnel. Ensure the service and tunnel remain running in the background. Leave the system ready for the automated verifier to test the endpoints.