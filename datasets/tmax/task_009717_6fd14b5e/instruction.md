As a capacity planner, I need you to build an automated metric collection pipeline for our legacy network services. We have an old interactive network daemon and a background worker process, and I need to correlate their resource usage.

Here is the current system state and your objectives:
1. There is a background worker process running named `worker_daemon.sh`.
2. There is a legacy network service listening on `127.0.0.1:9999`. It uses a custom interactive text protocol.

Please complete the following tasks:

**Phase 1: Port Forwarding**
The legacy daemon listens on port 9999, but our internal standard requires all metric collection to go through port `8080`. 
Run a background process using `socat` (or a similar user-space tool) to forward TCP connections from `127.0.0.1:8080` to `127.0.0.1:9999`.

**Phase 2: Interactive Automation**
Write an `expect` script at `/home/user/fetch_stats.exp` that connects to `127.0.0.1:8080`. The legacy daemon interaction works as follows:
- It prompts: `Username: ` -> You must send `admin`
- It prompts: `Password: ` -> You must send `cap_planner`
- It prompts: `CMD> ` -> You must send `STATS`
- It will return several lines of output, followed by another `CMD> ` prompt.
- You must send `QUIT` to exit gracefully.
The `expect` script should output the raw text returned by the `STATS` command to standard output.

**Phase 3: Text Processing and Process Monitoring**
Write a robust Bash script at `/home/user/collect_metrics.sh` that does the following:
1. Executes `/home/user/fetch_stats.exp` and captures its output.
2. Parses the active connections and bandwidth from the output using `awk`, `grep`, or `sed`. The daemon's stats output looks like:
   `[System Status]`
   `Active Connections: 142`
   `Current Bandwidth: 85 Mbps`
3. Uses `ps` to find the CPU% and Memory% (MEM%) of the `worker_daemon.sh` process.
4. Appends a single, comma-separated line to `/home/user/metrics.csv` with the following columns (in order, no spaces):
   `UNIX_TIMESTAMP,CONNECTIONS,BANDWIDTH_MBPS,WORKER_CPU_PERCENT,WORKER_MEM_PERCENT`
   Example output line: `1698000000,142,85,0.0,0.1`

**Phase 4: Execution**
Ensure `/home/user/collect_metrics.sh` is executable and run it exactly once so that `/home/user/metrics.csv` is created and contains exactly one line of data. 

*Note: All scripts should be well-formed. Handle potential errors gracefully. Do not use root/sudo.*