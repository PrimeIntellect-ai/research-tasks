You are an engineer diagnosing a user-level background service that crashes immediately upon starting. 

In `/home/user/app/`, there is a C source file `server.c` for a lightweight web service. 
In `/home/user/certs/`, there are mock TLS configuration files: `server.crt` and `server.key`.
There is a systemd user service configured at `/home/user/.config/systemd/user/secure-backend.service` intended to run this application.

Currently, the service fails to start. The issue is due to an environment variable mismatch: `server.c` relies on the `APP_CERTS_DIR` environment variable to locate its keys. When run from your interactive shell, this variable might be set, but within the systemd user service environment, it is null, causing the C application to segfault or fail.

Your tasks are to:
1. Identify and fix the bug in `/home/user/app/server.c` so that if `getenv("APP_CERTS_DIR")` returns NULL, it safely defaults to `/home/user/certs`. 
2. Compile the fixed C program to `/home/user/app/server`.
3. Fix the `secure-backend.service` file if necessary, reload the systemd user daemon, and start/enable the service.
4. The server listens on port `4433`. Set up a persistent, background SSH tunnel (using port forwarding) that forwards local port `8443` to the server's port `4433`. SSH to `localhost` is already configured with key-based authentication for the `user` account.
5. Create an idempotent bash script at `/home/user/setup.sh`. When run, this script must:
   - Compile `server.c` (only if the source has changed or the binary is missing).
   - Ensure the `secure-backend.service` is running and enabled.
   - Ensure the SSH tunnel from `8443` to `4433` is active (without spawning duplicate SSH processes if one is already running).
6. Verify the setup by running `curl http://localhost:8443/status` and saving the exact output to `/home/user/result.log`.

Do not use root privileges (`sudo`). All actions must be performed as the standard user.