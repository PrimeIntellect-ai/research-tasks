You are an observability engineer deploying a custom monitoring stack for a local email infrastructure. 

Currently, our legacy email daemon (`/home/user/mock_email_daemon.py`) handles internal alerts, but it is unstable and crashes occasionally. Additionally, it sits behind an internal "auth proxy" protocol that requires an injected token to process commands, acting much like a strict firewall or SSH config that silently rejects unauthenticated requests.

You need to implement a full deployment stack consisting of a process supervisor, a network routing proxy, and a metric exporter in Python.

Complete the following tasks:

1. **Process Supervisor (`/home/user/watchdog.py`)**:
   Write a Python script that launches and supervises `/home/user/mock_email_daemon.py`. 
   - It must run the daemon as a child process.
   - If the child process exits for any reason, the watchdog must immediately restart it.
   - Every time it restarts the process, it must append the exact string `[SUPERVISOR] daemon restarted` to `/home/user/watchdog.log` (on a new line).

2. **Network Routing Proxy (`/home/user/net_route.py`)**:
   The mock email daemon listens on `127.0.0.1:8025`, but it silently drops any connections that don't begin with a specific authorization token.
   Write a TCP proxy in Python that listens on `127.0.0.1:9025` and forwards bidirectional traffic to `127.0.0.1:8025`.
   - When a client connects to `9025`, the proxy must first connect to `8025` and send the string `AUTH_TOKEN: obs_admin\n` to the daemon *before* forwarding any client data.
   - After sending the token, it should transparently pipe data back and forth between the client and the daemon.

3. **Dashboard Metric Exporter (`/home/user/metric_exporter.py`)**:
   Write a Python script that polls the proxy to generate observability metrics.
   - Every 1 second, it should connect to `127.0.0.1:9025`.
   - It should read the initial SMTP banner.
   - It should send the command `EHLO monitor\r\n`.
   - If it receives a `250` response code from the `EHLO` command, it should append the string `email_service_up 1` (on a new line) to `/home/user/observability.log`.
   - It should then send `QUIT\r\n` and close the connection.
   - If the connection fails or it does not receive a `250` response, it should append `email_service_up 0` to `/home/user/observability.log`.

Do not start the scripts as background daemons in your final step; simply ensure the files are created with the correct logic. The automated test suite will execute them in the background to verify their behavior.