We have a local microservices stack managed by a custom Python script, but it is failing to start up correctly due to race conditions and missing dependency checks. The services are crashing because they start before their dependencies are ready.

Your task is to fix the Python process manager and integrate an SSH tunnel for our monitoring service.

Here is the setup in `/home/user/app`:
1. `db_service.py`: A mock database. When started, it initializes for 5 seconds, then listens on port `8001`.
2. `api_service.py`: A backend API. It requires port `8001` to be reachable immediately on startup; otherwise, it crashes. Once successful, it listens on port `8002`.
3. `monitor_service.py`: A monitoring tool that expects to connect to the API via a local port forward on port `9000`. If it succeeds, it writes `STATUS: ALL_SYSTEMS_GO` to `/home/user/app/monitor.log`.
4. `start_all.py`: The current (buggy) Python process manager that attempts to start all services simultaneously using `subprocess.Popen`.

Your objectives:
1. **Rewrite `start_all.py` (Python)**: Implement robust health checking. The script must start a process, actively check (poll) its target port until it is open and accepting connections, and only *then* start the dependent process.
2. **Setup an SSH Tunnel**: Inside `start_all.py`, after the `api_service.py` is ready on port `8002`, spawn a local SSH tunnel forwarding local port `9000` to `127.0.0.1:8002`. 
   - You must use the existing SSH key at `/home/user/.ssh/id_rsa` and connect as `user@127.0.0.1`.
   - Use SSH options `-N` and `-o StrictHostKeyChecking=no` to prevent prompts.
   - Wait for port `9000` to become active.
3. **Start the Monitor**: Finally, start `monitor_service.py`.
4. **Keep processes alive**: `start_all.py` should wait for all subprocesses to complete (or run indefinitely until interrupted). 

Run your fixed `start_all.py` so that it successfully brings up the stack in the background. Do not modify `db_service.py`, `api_service.py`, or `monitor_service.py`.

The task is complete when `/home/user/app/monitor.log` contains exactly:
`STATUS: ALL_SYSTEMS_GO`