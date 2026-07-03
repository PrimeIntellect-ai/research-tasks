You are a Linux systems engineer tasked with hardening a local storage service and building a process-monitoring daemon. You need to implement a storage quota monitor in Python and automate an interactive CLI tool using `expect`.

Phase 1: The Vault Monitor Daemon
Write a Python script at `/home/user/vault_monitor.py` that acts as a continuous background daemon. It must perform the following tasks:
1. Hardened Network Listener: Bind a TCP socket strictly to `127.0.0.1` on port `8443`. It should accept incoming connections. If a client sends the string "STATUS", it should reply with "OK\n" if the vault is under quota, or "LOCKED\n" if over quota.
2. Storage Monitoring: Every 1 second, calculate the total disk space used by all files in the directory `/home/user/vault/`.
3. Quota Enforcement: The quota is exactly 10,485,760 bytes (10 MB). If the total size of the vault strictly exceeds this quota, the daemon must immediately:
   a. Write a log file at `/home/user/vault_state.log` with the exact string: `LOCKED: <exact_total_bytes_in_vault>`
   b. Find any running process with `interactive_uploader.py` in its command line and terminate it using a SIGTERM signal.
4. Process Management: Upon startup, the script must write its own Process ID (PID) to `/home/user/monitor.pid`.

Phase 2: The Interactive Uploader Automation
A mock interactive uploader is located at `/home/user/interactive_uploader.py` (which already exists in your environment). 
Write an `expect` script at `/home/user/simulate_uploads.exp` that automates interactions with this tool to test your monitor daemon. The `expect` script must:
1. Spawn `python3 /home/user/interactive_uploader.py`.
2. Wait for the prompt: `Enter filename:` and send `payload1.bin`.
3. Wait for the prompt: `Enter size in bytes:` and send `6000000`.
4. Wait for the prompt: `Upload complete. Enter filename or type exit:` and send `payload2.bin`.
5. Wait for the prompt: `Enter size in bytes:` and send `5000000`.
6. Wait indefinitely (the monitor daemon should detect the quota breach and kill the process, causing the expect script to terminate).

Phase 3: Execution
1. Ensure the `/home/user/vault/` directory exists.
2. Run your `vault_monitor.py` in the background.
3. Run your `simulate_uploads.exp` script to trigger the quota breach.

Your success will be verified by checking for the correct PID file, the presence of the expected network listener, and the specific contents of `/home/user/vault_state.log`.