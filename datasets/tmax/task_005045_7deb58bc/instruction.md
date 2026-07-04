You are an ML Engineer preparing training data and A/B test results for a new algorithm. We have a multi-service pipeline that processes raw telemetry data, computes statistical metrics, and exposes them via an API.

There is a workspace prepared at `/home/user/app/` containing:
- `start_services.sh`: A script that starts a local Redis instance, an Nginx server, and a Python Uvicorn server for our FastAPI app.
- `nginx.conf`: The Nginx configuration file.
- `api.py`: A skeleton FastAPI application.
- `populate_redis.py`: A script to seed Redis with mock raw telemetry data.

Your tasks are:
1. **ETL & Statistical Modeling:**
   Complete the FastAPI application in `/home/user/app/api.py`. The app needs an endpoint `GET /stats`.
   When this endpoint is hit, it must:
   - Read all JSON strings from the Redis list `raw_telemetry` (Redis is running on `127.0.0.1:6379`, no password).
   - Parse the JSON objects, which look like `{"user_id": "...", "group": "A", "score": 85.5}`.
   - Separate the scores into two arrays: Group A and Group B.
   - Calculate the mean score for each group (`mean_A` and `mean_B`).
   - Perform a Welch's t-test (two-sided, unequal variances) to compare Group A and Group B scores, and extract the `p_value`.
   - Calculate the 95% Confidence Interval for the difference in means (`mean_B - mean_A`) using the standard normal approximation (Z=1.96): 
     `diff = mean_B - mean_A`
     `se = sqrt(var_B/n_B + var_A/n_A)`
     `ci_lower = diff - 1.96 * se`
     `ci_upper = diff + 1.96 * se`
     (Use sample variances, `ddof=1`).
   - Return a JSON response exactly like this:
     ```json
     {
       "mean_A": float,
       "mean_B": float,
       "p_value": float,
       "ci_lower": float,
       "ci_upper": float
     }
     ```

2. **Security & Protocol:**
   The `GET /stats` endpoint must be protected. It should only return the data if the request includes the HTTP header:
   `Authorization: Bearer secret-ml-token-99`
   If the token is missing or incorrect, return a `401 Unauthorized` status code. The FastAPI app will run on port `8000`.

3. **Multi-Service Composition:**
   Modify `/home/user/app/nginx.conf` so that Nginx (listening on port `8080`) acts as a reverse proxy. Any request to `http://127.0.0.1:8080/api/stats` should be internally routed to `http://127.0.0.1:8000/stats`. Ensure Nginx passes the `Authorization` header to the backend.

4. **Integration & Execution:**
   - Run `python /home/user/app/populate_redis.py` to seed the database.
   - Run `bash /home/user/app/start_services.sh` to start Redis, Nginx, and your FastAPI app.
   - Verify that you can successfully curl `http://127.0.0.1:8080/api/stats` with the correct bearer token and get the statistics. 

Leave the services running in the background when you are done so the automated verifier can test the API.