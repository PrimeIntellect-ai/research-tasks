You are an observability engineer trying to tune and fix a broken metrics dashboard pipeline on a Linux server.

Currently, we have a C-based metrics collector that runs periodically via a scheduler script, but the metrics dashboard is not updating. The collector is writing the metrics to the wrong location because it uses a relative path (`./metrics.json`), which causes it to write to the script's working directory instead of the dashboard's data directory. Furthermore, our internal dashboard service is only bound to localhost, and we need it exposed to our external scraper.

Your tasks are:

1. **Backup Strategy**: 
   Before making any changes, copy the original source code `/home/user/src/collector.c` to `/home/user/backup/collector.c.bak`.

2. **Fix the C Application**:
   Modify the C source code at `/home/user/src/collector.c`. Change the file output path from `./metrics.json` to the absolute path `/home/user/dashboard/metrics.json`.
   Recompile the C code using `gcc` and overwrite the existing binary at `/home/user/bin/collector`.

3. **Port Forwarding (Observability Scraper)**:
   The dashboard HTTP server runs locally on `127.0.0.1:8080`. You need to set up a lightweight local port forwarder (since you don't have root access for iptables) so that traffic to `127.0.0.1:9090` is forwarded to `127.0.0.1:8080`. 
   Use `socat` to accomplish this. Run the `socat` command in the background and save its process ID (PID) to `/home/user/proxy.pid`.

4. **Verify Collection**:
   Execute the recompiled binary `/home/user/bin/collector` once manually to ensure it generates `/home/user/dashboard/metrics.json` correctly.

Constraints & Details:
- The dashboard directory `/home/user/dashboard/` and backup directory `/home/user/backup/` already exist.
- Do not modify the `cron_task.sh` script; only modify and recompile the C code.
- Ensure the `socat` process forks into the background and stays running. Use a command like `socat TCP4-LISTEN:9090,bind=127.0.0.1,reuseaddr,fork TCP4:127.0.0.1:8080 & echo $! > /home/user/proxy.pid`.