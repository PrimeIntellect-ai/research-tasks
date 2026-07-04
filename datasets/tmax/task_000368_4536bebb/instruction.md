You are an ML Engineer preparing a robust data pipeline to evaluate incoming training data matrices for data drift. We have a microservice architecture located in `/app/` managed by a custom `supervisor.conf`.

The system consists of:
1. **Ingestion API**: A Python service on port 8001 that receives JSON payloads containing data matrices and pushes them to a Redis queue (`incoming_matrices`).
2. **Redis**: Running on `localhost:6379`.
3. **Webhook API**: A Node.js service on port 8002 that receives processed results and serves them on a `/metrics` endpoint.
4. **Nginx**: A reverse proxy that should be configured to route traffic to these APIs.

Your task is to fix the configuration and write the core processing worker in Bash.

**Step 1: Configure Nginx**
Edit `/etc/nginx/nginx.conf` (or the relevant site config in `/app/nginx/`) so that:
- Requests to `http://localhost:8080/ingest` route to the Ingestion API on port 8001.
- Requests to `http://localhost:8080/results` route to the Webhook API on port 8002.
- The Nginx service must run as a daemon.

**Step 2: Write the Bash Processing Worker**
Create a Bash script at `/app/worker.sh` that continuously monitors the Redis `incoming_matrices` list (using `redis-cli blpop`). For each JSON matrix popped:
1. Extract the matrix.
2. Use Python (inline or as a separate script called by the Bash worker) to compute the Singular Value Decomposition (SVD).
3. Extract the singular values and compare them to a baseline distribution (provided in `/app/baseline_singular_values.csv`).
4. Calculate the Wasserstein distance and perform a 2-sample Kolmogorov-Smirnov (KS) test between the incoming singular values and the baseline.
5. Create a JSON payload with the following format:
   `{"id": "<matrix_id>", "wasserstein_distance": <float>, "ks_pvalue": <float>, "drift_detected": <true/false>}`
   *Note: `drift_detected` should be `true` if the KS p-value < 0.05.*
6. POST this JSON payload to the Webhook API at `http://localhost:8002/report` using `curl` with header `Authorization: Bearer secret-ml-token`.

**Step 3: Start the Services**
Ensure all services (Redis, Ingestion API, Webhook API, Nginx, and your Bash worker) are running. You can start the pre-existing services using the provided `/app/start_services.sh` script, but you will need to launch your worker and Nginx manually or add them to the script.

Leave the services running. Our automated testing suite will send HTTP POST requests to `http://localhost:8080/ingest` and verify the metrics at `http://localhost:8080/results`.