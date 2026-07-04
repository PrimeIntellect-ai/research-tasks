You are acting as a FinOps engineer migrating a set of expensive cloud billing functions to a lightweight, optimized local stack to reduce operational costs. 

In `/home/user/app/`, there are three components of this stack:
1. `billing_datastore.py`: A Python backend service that returns cost metrics.
2. `cost_analyzer.py`: A Python service that aggregates data from the datastore.
3. `nginx.conf`: An Nginx configuration file meant to serve as the reverse proxy for the analyzer.

Currently, the services cannot communicate, the reverse proxy is misconfigured, and there is no process monitoring in place.

Your objective is to fix the deployment so the end-to-end API works.

Complete the following steps:
1. **Environment Setup:** The `cost_analyzer.py` service expects the environment variables `DATASTORE_HOST`, `DATASTORE_PORT`, and `FINOPS_API_KEY` to be set. The datastore runs on `localhost` port `9092`. The API key must be set to `opt-cost-2024`. Export these in `/home/user/.bashrc` and ensure they are active.
2. **Reverse Proxy Configuration:** Edit `/home/user/app/nginx.conf`. Configure it to run on port `8080` (as a non-root user). Set up a reverse proxy block so that any HTTP GET request to `/api/v1/costs` is routed to the `cost_analyzer.py` service, which listens on port `9091`. Ensure Nginx stores its PID file at `/home/user/app/nginx.pid` and uses `/home/user/app/error.log` for logs to avoid permission issues.
3. **Service Management:** Write a bash script at `/home/user/app/start_all.sh` that:
   - Starts `billing_datastore.py` in the background.
   - Starts `cost_analyzer.py` in the background.
   - Starts Nginx using the local `nginx.conf` file.
   - Includes basic process monitoring: an infinite loop that checks if Nginx (port 8080) and the cost analyzer (port 9091) are responding. If Nginx dies, the script should restart it.
4. **Integration:** Run your `start_all.sh` script. 

An automated verifier will eventually test your setup by sending HTTP requests to `http://localhost:8080/api/v1/costs`.