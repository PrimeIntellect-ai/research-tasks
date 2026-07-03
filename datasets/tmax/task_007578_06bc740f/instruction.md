You are a Site Reliability Engineer (SRE) investigating an uptime alert. Our uptime monitoring system has detected that the primary API gateway is intermittently returning `502 Bad Gateway` errors.

The system consists of two microservices running locally:
1. **Frontend Service (Node.js)**: Listens on `http://localhost:8080` and proxies requests to the backend.
2. **Backend Service (Python)**: Listens on `http://localhost:8081` and serves system status.

Both services are located in `/home/user/services/`. There is a launcher script `/home/user/services/start.sh` that starts the services and automatically restarts the backend if it crashes.

Your task:
1. Start the services using `/home/user/services/start.sh`.
2. Reproduce the intermittent 502 errors (you may need to send a moderate amount of traffic to the frontend to trigger it).
3. Reconstruct the timeline of the failure by analyzing the service logs (`/home/user/services/frontend.log` and `/home/user/services/backend.log`).
4. Use system call tracing (`strace`) on the failing process to identify the exact system call and error code causing the crashes.
5. Fix the root cause of the bug in the source code so the service can run indefinitely without crashing under load.
6. Create a Root Cause Analysis (RCA) report at `/home/user/rca.json` containing exactly this JSON structure:
   ```json
   {
     "failing_component": "<'frontend' or 'backend'>",
     "failing_syscall": "<the exact system call that fails and triggers the crash, e.g., read, openat, socket>",
     "errno": "<the exact error code constant returned by the syscall, e.g., ENOENT, EMFILE, ENOMEM>"
   }
   ```

Constraints:
- Do not change the ports or the overall architecture.
- Do not use `ulimit` to simply mask the issue; you must fix the underlying code defect.