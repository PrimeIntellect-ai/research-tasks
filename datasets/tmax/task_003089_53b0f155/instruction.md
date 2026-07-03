You are tasked with migrating a legacy user authentication system for an internal site. We have an old, stripped binary located at `/app/legacy_auth` that verifies user credentials. 

Your objective is to build a modern facade in Python that exposes this legacy authentication via an SSH service and a status API. 

Here are the requirements:

1. **Investigate `/app/legacy_auth`:**
   The binary is a black-box stripped executable. It accepts arguments to verify a user's password. You need to figure out its exact calling convention and expected output by analyzing it (e.g., using `strings`, `strace`, or passing test inputs). 

2. **Python SSH Facade (Port 2222):**
   Write a Python script at `/home/user/auth_facade.py` that starts a custom SSH server on `0.0.0.0:2222`. You may use libraries like `paramiko` or `asyncssh` (install them via pip).
   - **Password Authentication:** The SSH server must accept password authentication ONLY if the `/app/legacy_auth` binary validates the username and password successfully.
   - **Key-based Authentication:** The SSH server must silently reject all public key authentication attempts.
   - **Session:** Upon successful password login, the SSH server should not provide a full shell. Instead, it must send the exact string `Welcome <username>` to the client and immediately close the connection.

3. **HTTP Status API (Port 8080):**
   Within the same Python script (or as a separate process managed by it), expose an HTTP server on `0.0.0.0:8080`.
   - `GET /health` must return an HTTP 200 response with the text `OK`.

4. **Lifecycle Management:**
   Write a bash script `/home/user/start_services.sh` that securely generates any necessary SSH host keys (e.g., at `/home/user/host_key`), starts your Python service(s) in the background, and outputs their PIDs to `/home/user/service.pid`.

Make sure your services are running and listening on the specified ports before you finish the task. The automated verification will connect to your SSH server and HTTP API to test functionality.