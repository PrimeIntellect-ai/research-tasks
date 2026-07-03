You are a security researcher analyzing a suspicious composed system found on a compromised server. The system consists of a C++ proxy service (`proxy_daemon`) and a Python backend service (`backend.py`). 

Recently, the proxy has been crashing or hanging, seemingly due to a resource leak when connections are abruptly cancelled (similar to a goroutine leak under cancellation, but here leaking file descriptors or threads). 

Your goals are:
1. **Analyze the composed system**: The services are located in `/app/services/`. You can start them using `/app/services/start_all.sh`. The proxy listens on port `9000` (HTTP) and `9002` (raw TCP management), and routes traffic to the backend on `9001`.
2. **System Call Tracing & Delta Debugging**: A large payload script `/app/payloads/trigger_crash.sh` reliably brings down the proxy after 500 requests. Trace the proxy using `strace` or similar tools to find the exact resource leak. Minimize the trigger down to a single `curl` or `nc` command that leaks exactly ONE resource (e.g., a file descriptor) per execution. Save this minimized command in `/home/user/minimal_repro.sh`.
3. **Git Bisection**: The proxy source code is in a Git repository at `/app/services/proxy_src/`. Use `git bisect` to find the exact commit that introduced the leak. Write the full commit hash to `/home/user/bad_commit.txt`.
4. **Convergence Failure Repair**: Fix the C++ source code in `/app/services/proxy_src/main.cpp` so that it properly handles dropped connections without leaking file descriptors or threads.
5. **Re-integration**: Recompile the proxy daemon (`make` in the src directory) and restart the composed services. 

Ensure the services are running when you finish. Automated verifiers will connect to:
- Port `9000` (HTTP): Sending standard GET requests, which should return `200 OK` from the backend.
- Port `9000` (HTTP): Sending partial/aborted requests to ensure the system no longer leaks file descriptors.
- Port `9002` (TCP): Sending the raw command `STATUS\n`, which should reply with `PROXY_OK\n`.

Do not change the ports or the backend logic. Fix only the C++ proxy daemon.