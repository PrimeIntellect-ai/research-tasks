You are tasked with fixing a deployment issue for a critical data processing daemon written in C, and implementing a robust process supervision script to keep it running.

Currently, the C daemon reads strings from a named pipe (FIFO) and processes them. However, it crashes (segmentation fault) when it receives malformed payloads. Your objective is to patch the C code, recompile it, and write a Bash supervisor script that acts as a simple process manager (simulating a container restart policy).

Here is the current state of the system:
- A directory exists at `/home/user/deploy`
- The source code is located at `/home/user/deploy/daemon.c`
- A named pipe exists at `/home/user/deploy/data.fifo`

Perform the following tasks:

1. **Fix the C Daemon**: 
   The program `daemon.c` is designed to read lines from `/home/user/deploy/data.fifo` and append the processed lines to `/home/user/deploy/processed.log`. 
   However, if the daemon reads the exact string "POISON", it dereferences a NULL pointer and crashes.
   Modify `/home/user/deploy/daemon.c` so that if it reads "POISON", it simply ignores that line, continues processing the next lines, and DOES NOT crash. 
   Compile your fixed code to an executable named `/home/user/deploy/daemon_exec` using `gcc`.

2. **Create a Supervisor Script**:
   Create a bash script at `/home/user/deploy/supervisor.sh` with executable permissions. This script must:
   - Run `/home/user/deploy/daemon_exec` in the foreground.
   - If `daemon_exec` exits with a non-zero exit code (e.g., if it crashes or is killed), the supervisor must append the exact line `[WARN] Daemon crashed. Restarting...` to `/home/user/deploy/supervisor.log`, and immediately restart `daemon_exec`.
   - If `daemon_exec` exits with a clean exit code of `0` (which happens if it receives the string "SHUTDOWN" from the FIFO), the supervisor script should append `[INFO] Daemon shut down cleanly.` to `/home/user/deploy/supervisor.log` and then the supervisor script itself should exit with code 0.

Ensure your compiled executable and the supervisor script are ready. You do not need to leave the supervisor running in the background; the automated test will invoke `/home/user/deploy/supervisor.sh` and push data into the FIFO to verify its behavior and your code fixes.