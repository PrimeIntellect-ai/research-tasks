You are a monitoring specialist tasked with ensuring the reliability of a brittle internal web service. 

A legacy service is located at `/home/user/legacy_service/`. It is started via the script `/home/user/legacy_service/start.sh`. The service binds to `127.0.0.1:8888`. Unfortunately, this service is unstable and crashes frequently.

Your task is to write a robust Python script named `/home/user/monitor.py` that acts as a process supervisor and alerting mechanism.

Requirements for `/home/user/monitor.py`:
1. It must run continuously in an infinite loop.
2. Every 1 second, it must attempt to establish a TCP connection to `127.0.0.1:8888` (with a 1-second timeout).
3. If the connection fails (e.g., connection refused or timeout) for **3 consecutive attempts**, the script must:
   a. Append an alert to `/home/user/monitoring.log` in this exact format:
      `ALERT: Service failure detected at <UNIX_TIMESTAMP>`
      (where `<UNIX_TIMESTAMP>` is the integer Unix time, e.g., `1697040000`).
   b. Execute the script `/home/user/legacy_service/start.sh` to restart the service.
   c. Wait until the service successfully accepts a TCP connection on port 8888 again before resuming the standard 1-second polling loop.
4. The monitor script should be robust and gracefully handle the service being down without crashing itself.
5. If the service is already running when `monitor.py` starts, it should simply monitor it; it should not blindly execute `start.sh` unless the 3-failure condition is met.

Before you finish, ensure that `/home/user/monitor.py` is running in the background and that it has successfully detected at least one simulated crash and recovered the service. You can trigger a crash manually or let the legacy service crash on its own (it crashes after a few connections).