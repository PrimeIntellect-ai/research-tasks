You are an infrastructure engineer tasked with setting up a capacity planning metric ingestion pipeline and rewriting a legacy analysis tool.

Part 1: Metric Pipeline Setup (Multi-Service)
We have a local metric ingestion system consisting of an Nginx load balancer and two Flask receiver instances. They are provided in `/app/services/` but are not correctly configured.
1. Create a directory structure for logs: `/home/user/metrics_data/raw`. Ensure that ONLY the owner has read, write, and execute permissions (chmod 700) on `/home/user/metrics_data` and its subdirectories.
2. Create a symlink at `/home/user/active_metrics` pointing to `/home/user/metrics_data/raw`.
3. Configure Nginx (config file at `/home/user/nginx.conf`) to listen on port 8080. It should load balance requests for the path `/ingest` across two upstream servers: `127.0.0.1:5001` and `127.0.0.1:5002`. Add a basic health check configuration in Nginx (`max_fails=3 fail_timeout=10s`) for these upstreams.
4. The Flask apps are started via a script `/app/start_services.sh`. You need to set the environment variable `METRICS_DIR=/home/user/active_metrics` before running or configuring them, so they write their logs to the symlinked directory. Run `/app/start_services.sh` in the background. Nginx should be started with your config: `nginx -c /home/user/nginx.conf`.

Part 2: Legacy Analyzer Rewrite (Fuzz Equivalence)
We have a legacy compiled binary at `/app/oracle_planner` that processes raw metric text logs from standard input and prints a capacity report to standard output. We lost the source code and need you to rewrite it in Python.
Create a Python script at `/home/user/planner.py` that exactly replicates the behavior of `/app/oracle_planner`.

The input format (read from `sys.stdin`) consists of multiple lines. Each line is formatted as:
`TIMESTAMP SERVICE_NAME METRIC_NAME VALUE`
Example:
`1680001000 frontend cpu 85.5`
`1680001005 backend mem 1024.0`

Your script must:
1. Ignore any line where `VALUE` is strictly less than 0.
2. Group the remaining records by `SERVICE_NAME` and `METRIC_NAME`.
3. For each group, calculate the Maximum value and the Average value.
4. The Average must be rounded DOWN to the nearest integer (using floor). The Maximum should be formatted to exactly 2 decimal places.
5. Print the results to standard output, one per line, sorted alphabetically by `SERVICE_NAME`, then alphabetically by `METRIC_NAME`.
Format of output lines:
`SERVICE_NAME METRIC_NAME MAX: <max_val>, AVG: <avg_val_floored>`

Example Output:
`backend mem MAX: 1024.00, AVG: 1024`
`frontend cpu MAX: 85.50, AVG: 85`

Your Python script must be executable (`chmod +x`) and have the correct shebang (`#!/usr/bin/env python3`).