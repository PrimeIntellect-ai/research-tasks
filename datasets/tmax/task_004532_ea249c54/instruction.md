You are a FinOps engineer working to optimize cloud networking costs. Our current infrastructure routes all API data processing to an expensive, high-performance backend, regardless of priority. We want to implement a cost-aware routing proxy in Rust.

There is a multi-service setup located in `/home/user/app/`:
1. `backend_expensive` (Listens on HTTP `127.0.0.1:8081`) - Fast, expensive processing tier.
2. `backend_cheap` (Listens on HTTP `127.0.0.1:8082`) - Slow, cheap spot-instance tier.
3. `nginx` (Listens on HTTP `127.0.0.1:8080`) - The front-facing load balancer.

Your tasks are:

1. **Implement the Cost-Aware Proxy (Rust):**
   In `/home/user/proxy`, there is an incomplete Rust web server project (using `axum` and `tokio`). 
   Update the code so the proxy:
   - Listens for HTTP traffic on `127.0.0.1:8083`.
   - Accepts POST requests on `/process`.
   - Inspects the `X-Tier` header. If `X-Tier: Spot` is present, it forwards the exact request body to `http://127.0.0.1:8082/process` and returns its response. If `X-Tier: OnDemand` is present, or the header is missing, it forwards it to `http://127.0.0.1:8081/process` and returns its response.
   - Maintains a running count of all processed requests.
   - Exposes a secondary TCP admin server on `127.0.0.1:8084`. When a TCP client connects and sends the exact string `STATS\n`, it must reply with `PROCESSED={count}\n` (where `{count}` is the total number of processed HTTP requests) and close the connection.

2. **Configure Nginx for Staged Deployment:**
   Modify the Nginx configuration at `/home/user/app/nginx.conf` so that all traffic hitting `http://127.0.0.1:8080/process` is proxied to your new Rust proxy at `127.0.0.1:8083`.

3. **Write a Deployment Automation Script:**
   Create an automation script at `/home/user/deploy.sh` (make it executable) that:
   - Compiles the Rust proxy in release mode.
   - Starts the Rust proxy in the background, redirecting stdout/stderr to `/home/user/proxy.log`.
   - Uses connectivity diagnostics (e.g., `nc`, `curl`, or `bash -c`) to poll the TCP admin port (`8084`) every 1 second until it responds to a connection, ensuring the proxy is fully up.
   - Reloads the local Nginx instance (using the provided script `/home/user/app/reload_nginx.sh`).

4. **Write a Backup Script:**
   Create a script at `/home/user/backup.sh` that securely backs up `/home/user/proxy.log` to `/home/user/backups/proxy_$(date +%s).log.gz` using gzip. Create the `/home/user/backups/` directory if it does not exist.

Once you have written the code and scripts, run `/home/user/deploy.sh` to start the infrastructure. Leave the proxy and nginx running.