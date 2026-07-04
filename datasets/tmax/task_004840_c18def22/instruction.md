As a capacity planner, I need to automate the deployment of a local web service, expose it via port forwarding, and monitor its resource usage to baseline its footprint. 

Please create a Bash script at `/home/user/deploy_and_monitor.sh` that performs the following steps exactly:

1. Create a directory `/home/user/app` and write a simple file named `index.html` inside it containing the text "OK".
2. Start a Python HTTP server (`python3 -m http.server 8443`) in the background, serving the `/home/user/app` directory.
3. Use `socat` to forward TCP port `9443` to `localhost:8443` in the background (simulate port forwarding).
4. Wait for 2 seconds to allow the services to start.
5. Create a CSV file at `/home/user/metrics.csv` with the header: `TIMESTAMP,PID,RSS_KB`
6. Run a monitoring loop exactly 3 times, with a 1-second `sleep` between iterations. In each iteration:
   - Make a `curl -s http://localhost:9443/` request and discard the output (to generate minor load).
   - Use `ps` to find the RSS (Resident Set Size in KB) of the Python HTTP server process.
   - Append a line to `/home/user/metrics.csv` with the current Unix epoch timestamp, the Python server's PID, and its RSS usage.
7. After the 3 monitoring loops, gracefully terminate both the `python3` server and the `socat` process.

Make sure the script is executable (`chmod +x`). I will test your work by executing `/home/user/deploy_and_monitor.sh` and then inspecting `/home/user/metrics.csv` and checking that no stray background processes were left running.