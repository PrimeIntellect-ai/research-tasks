You are a system administrator diagnosing a broken multi-service pipeline. 

The system relies on a startup script at `/app/system/start_services.sh` which brings up:
1. A QEMU VM running an internal analytics backend. The VM's SSH is exposed on `localhost:2222` (username: `vmsvc`, password: `password123`). The internal backend listens on port `80` inside the VM.
2. A local supervisor process that continuously attempts to compile and run a C-based sanitization proxy located at `/home/user/sanitizer.c`.

Currently, the pipeline is completely broken:
- The C sanitizer fails to start because its wrapper script (`/home/user/run_sanitizer.sh`) does not export the required locale (`LANG=en_US.UTF-8`), timezone (`TZ=UTC`), and environment variable `BACKEND_PORT=9000`. You must fix `/home/user/run_sanitizer.sh` so it sets these variables and then executes the compiled `./sanitizer` binary.
- The C proxy expects the backend to be reachable on `localhost:9000`. You must establish a persistent SSH tunnel forwarding local port `9000` to port `80` inside the QEMU VM via the SSH port `2222`.
- The C program `/home/user/sanitizer.c` is incomplete. You must implement the filtering logic. The program will be invoked as `./sanitizer <filepath>`. It must read the file. If the file contains the exact string `EVIL_PAYLOAD` or any backticks (`` ` ``), the program must print "REJECTED" to stdout and exit with status code `1`. If the file is clean, it must print "ACCEPTED" and exit with status code `0`. (The local supervisor handles the actual forwarding once it sees a 0 exit code).

**Your tasks:**
1. Establish the SSH tunnel so `localhost:9000` routes to the VM's port `80`.
2. Fix `/home/user/run_sanitizer.sh` to include the required environment variables, timezone, and locale settings before running the binary.
3. Complete `/home/user/sanitizer.c` to properly classify files as clean or evil according to the rules above. Compile it to `/home/user/sanitizer`.

Ensure the tunnel is active and the C program correctly classifies files. The automated test will test your compiled `/home/user/sanitizer` binary against a secret corpus of clean and evil files.