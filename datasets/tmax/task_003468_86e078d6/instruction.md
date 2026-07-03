You are an observability engineer tasked with tuning dashboards and ensuring high availability for a legacy email dispatch service. To do this without rewriting the core service, you need to write a custom C++ process supervisor that manages the mock "container" processes, handles rolling deployments, and provides metric logs for your dashboard.

Your objective is to write a C++ program at `/home/user/workspace/mda_supervisor.cpp` and compile it to an executable named `/home/user/workspace/mda_supervisor`.

**Requirements for `mda_supervisor`:**
1. **Process Supervision:**
   - The supervisor must manage exactly 3 instances of a mock Mail Delivery Agent (MDA).
   - The MDA executable is provided at `/home/user/mda.sh`. It takes two positional arguments: `instance_id` (1, 2, or 3) and `version` (e.g., "v1.0").
   - On startup, the supervisor should spawn the 3 instances using `fork()` and `execvp()`, starting them with version "v1.0".
   - It must continuously monitor these child processes (e.g., using `waitpid`). 
   - If a child crashes (exits with a non-zero status or is killed by an abnormal signal), the supervisor must automatically restart it with its current version.

2. **Observability Logs:**
   - Every time a child process is started, crashes, or is gracefully stopped, append a single line to `/home/user/dashboard_metrics.log`.
   - The format must strictly match:
     `INSTANCE <id> VERSION <version> EVENT <START|CRASH|GRACEFUL_STOP>`

3. **Email Alerting:**
   - If any single instance experiences **2 crashes** in its lifetime, the supervisor must immediately generate an email alert file in the local outbox directory `/home/user/mail/outbox/`.
   - The file must be named `alert_<id>.eml` (e.g., `alert_2.eml` for instance 2).
   - The content of the file must exactly match:
     ```
     To: admin@local
     Subject: Alert Instance <id>

     Crash loop detected for instance <id> version <version>.
     ```

4. **Rolling Deployments:**
   - The supervisor must handle the `SIGUSR1` signal to trigger a rolling deployment.
   - When `SIGUSR1` is received, it must read the target version string from `/home/user/next_version.txt`.
   - It must perform a staged, rolling rollout: for each instance (sequentially from 1 to 3):
     1. Send `SIGTERM` to the old process.
     2. Wait for it to exit (this should trigger a `GRACEFUL_STOP` log entry, NOT a `CRASH`).
     3. Start the new instance with the new version read from the file (triggering a `START` log entry).
   - The supervisor must ensure the old instance has fully terminated before starting the new instance for that specific ID.

**Constraints:**
- Use C++11 or later. Compile with `g++ -std=c++11 /home/user/workspace/mda_supervisor.cpp -o /home/user/workspace/mda_supervisor`.
- Do not use external libraries (standard POSIX C/C++ libraries only: `<unistd.h>`, `<sys/wait.h>`, `<csignal>`, `<fstream>`, etc.).
- Ensure your signal handlers are safe and your main loop properly handles the asynchronous nature of `waitpid` and signals.
- The working directories `/home/user/workspace` and `/home/user/mail/outbox` already exist. `/home/user/mda.sh` already exists.