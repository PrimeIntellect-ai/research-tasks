You are acting as a FinOps analyst tasked with optimizing and monitoring cloud costs. You have a raw billing export, and you need to build a small monitoring pipeline to expose the costs of active resources.

Perform the following steps:

1. **Text Processing Pipeline**:
   You have a raw billing CSV file at `/home/user/billing_raw.csv`. The columns are `id,service,region,status,cost`.
   Use command-line text processing tools (like awk, grep, sed) to filter this file. You must extract only the rows where the `status` (4th column) is exactly `ACTIVE` and the `cost` (5th column) is strictly greater than `0`.
   Save the filtered output (without any headers, just the matching data rows) to `/home/user/billing_active.csv`.

2. **Go Monitoring Service**:
   Write a Go program at `/home/user/finops_monitor.go` that does the following:
   - Reads the `/home/user/billing_active.csv` file.
   - Aggregates the total cost (column 5) grouped by the `service` name (column 2).
   - Starts an HTTP web server listening on `127.0.0.1:9090`.
   - Exposes a health check endpoint at `/health` that returns an HTTP 200 status code with the exact plain text body `OK`.
   - Exposes a metrics endpoint at `/metrics` that returns the aggregated costs in a Prometheus-like plain text format: `cost{service="<SERVICE_NAME>"} <TOTAL_COST>` (one per line, e.g., `cost{service="EC2"} 150.50`). The costs should be formatted to two decimal places.
   
   Compile the program to `/home/user/finops_monitor` and start it in the background.

3. **Port Forwarding**:
   Because of local network policies, external scrapers expect the metrics on port `8080`. Since you don't have root access to configure `iptables`, use `socat` to forward TCP connections from `127.0.0.1:8080` to your Go service at `127.0.0.1:9090`. Start this `socat` process in the background.

4. **Health Check and Verification**:
   Write a shell script at `/home/user/check_health.sh` that:
   - Performs a `curl` request to the `/health` endpoint via the forwarded port (`http://127.0.0.1:8080/health`).
   - If the response is exactly `OK`, it performs a `curl` request to the `/metrics` endpoint (`http://127.0.0.1:8080/metrics`), sorts the output alphabetically, and saves the sorted output to `/home/user/final_metrics.txt`.
   
   Execute the `/home/user/check_health.sh` script so that `/home/user/final_metrics.txt` is generated.