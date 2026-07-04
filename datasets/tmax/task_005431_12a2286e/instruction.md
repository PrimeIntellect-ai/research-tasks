You are tasked with implementing a "Policy as Code" payload inspection pipeline. We have a legacy architecture receiving encoded telemetry payloads, and we need to securely decode, filter, and forward these payloads to a backend data store.

Your objective is to write the core payload decoder in C, configure its process isolation, and glue together the end-to-end service flow.

Phase 1: Payload Decoder (C)
Write a C program at `/home/user/policy_decoder.c` and compile it to `/home/user/policy_decoder`.
This program must act exactly like our closed-source reference binary (`/app/oracle_decoder`).
The program requirements are:
- It reads a single line of input from `stdin` containing a hex-encoded string (e.g., "48656c6c6f").
- It decodes the hex string into raw bytes.
- It decrypts the bytes using a simple XOR cipher with the static key `0x5A`.
- If the decrypted raw string contains the exact sequence `MALICIOUS_DROP`, the program must print `POLICY_VIOLATION` to `stderr` and exit with status code 42.
- Otherwise, it must print the decrypted string to `stdout` and exit with status code 0.
- Ensure the program handles inputs up to 4096 characters gracefully.

Phase 2: Process Isolation and Sandboxing
We cannot trust the payloads or the decoder process. You must create a wrapper script at `/home/user/sandbox_wrapper.sh` that takes the hex payload as its first argument and passes it to the `policy_decoder` via `stdin`, but the decoder must be run inside a restricted `bwrap` (bubblewrap) sandbox.
The `bwrap` invocation must:
- Bind mount `/usr`, `/lib`, `/lib64`, and `/bin` read-only.
- Mount a temporary `tmpfs` at `/tmp`.
- Map the current working directory read-only.
- Drop all network access (`--unshare-net`).
- Execute `/home/user/policy_decoder`.

Phase 3: Multi-Service Pipeline
There are three services defined in `/app/start_services.sh` (which is already running):
1. An Nginx reverse proxy listening on port 8080.
2. A Python Flask intermediary service listening on port 5000 (source code at `/home/user/flask_app.py`).
3. A Redis backend on port 6379 (requires password `SecureRedis99!`).

You need to modify `/home/user/flask_app.py` to:
- Accept POST requests on `/submit` with a JSON body: `{"payload": "<hex_string>"}`.
- Pass the `<hex_string>` to your `/home/user/sandbox_wrapper.sh`.
- If the wrapper exits with code 42, return an HTTP 403 response with text "Blocked".
- If the wrapper exits with code 0, take the decoded `stdout` output, save it to the Redis backend in a list named `telemetry_logs`, and return HTTP 200 with text "Accepted".

Configure Nginx (`/home/user/nginx.conf`) to route all traffic from port 8080 to the Flask app on port 5000. Reload Nginx to apply changes. Ensure the end-to-end flow is fully operational.