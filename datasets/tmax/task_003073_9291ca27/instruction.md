We have an urgent IT support ticket (Ticket #8849) regarding our real-time anomaly detection pipeline located in `/app/anomaly_pipeline`. 

The pipeline consists of three services:
1. A Redis cache for storing intermediate time-series data.
2. A Flask API Gateway listening on `127.0.0.1:8080`.
3. A Python background worker that pulls data from Redis, computes statistical bounds using a custom iterative algorithm, and pushes the results back to Redis.

Recently, users reported that the anomaly scores returned by the API are suddenly showing statistical anomalies of their own—failing to converge or returning severely truncated values. We suspect a recent commit in the worker repository (`/app/anomaly_pipeline/worker_repo`) introduced a floating-point precision error or a convergence failure.

Your task is to:
1. Navigate to `/app/anomaly_pipeline/worker_repo`. It is a local git repository. Use `git bisect` to find the exact commit that introduced the regression. The good commit is tagged `v1.0`, and `HEAD` is known to be bad. A test script `test_convergence.py` is available in the repo root to verify if a commit is good or bad (it exits with 0 on success).
2. Once you identify the bad commit, diagnose the floating-point precision issue or convergence failure introduced in `compute_engine.py`. Fix the code so it correctly uses double precision (float64) instead of accidentally truncating to float32, and ensure the iterative loop converges properly.
3. Commit your fix to the repository on the main branch.
4. The services are managed by a startup script `/app/anomaly_pipeline/start_services.sh`. The worker is currently configured to connect to the wrong Redis port due to a misconfiguration in `/app/anomaly_pipeline/config.json`. Fix the port in the config to match the actual Redis instance running on port `6379`.
5. Restart the services using the provided `restart_all.sh` script.
6. Verify the system is working. Send a POST request to `http://127.0.0.1:8080/api/v1/analyze` with a JSON payload `{"series_id": "test_123"}`. The API requires an Authorization header with the Bearer token `IT-SUPPORT-AUTH-992`.

Finally, write the full hash of the bad commit you found into `/home/user/bad_commit.txt`, and the final correct JSON response from the API into `/home/user/api_response.json`.