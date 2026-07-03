You are a data engineer responsible for fixing and deploying a local ETL pipeline. The pipeline ingests financial transaction events, cleanses them, and persists them. We are currently facing issues with downstream data poisoning due to malicious and malformed payloads, as well as configuration issues in our service composition.

The system consists of three services running locally:
1. An ingestion API written in Flask (located in `/home/user/app/flask_api/`).
2. A Redis instance acting as a message queue.
3. A C++ ETL Worker that you need to write and compile.

Your objectives are:

1. **Service Composition & Configuration:**
   - The Flask API is supposed to receive HTTP POST requests on port 8080 and push the raw JSON payloads to a Redis list called `etl:input`.
   - Currently, the Flask app (`/home/user/app/flask_api/app.py`) is misconfigured and failing to connect to Redis. Fix the configuration / environment variables so it properly queues incoming POST requests to `etl:input`.
   - Ensure both Redis and the Flask application are running in the background.

2. **C++ ETL Worker & Statistical Filtering:**
   - Write a C++ program at `/home/user/etl_worker.cpp` (and compile it to `/home/user/etl_worker`).
   - The worker must continuously `BLPOP` from the Redis list `etl:input`.
   - Each payload is a JSON string containing at least `transaction_id` (string), `user_id` (string), and `amount` (numeric). 
   - **Missing Value Handling:** If `user_id` is missing or null, impute it with the string `"UNKNOWN"`. If `amount` is missing, null, or a non-numeric type, the payload is invalid and must be rejected.
   - **Outlier Handling via Bootstrap Sampling:** To detect adversarial/poisoned data, maintain a rolling history of the last 50 valid `amount` values. For each new incoming transaction, perform a bootstrap sampling routine (e.g., 100 resamples with replacement from the history to compute the 99th percentile of the mean or a robust confidence interval). Reject the transaction if its `amount` exceeds 3 standard deviations of your bootstrap distribution or a similarly rigorous dynamic bound. (For the first 50 transactions, accept them automatically unless they are missing the `amount`).
   
3. **Routing and Logging:**
   - Write accepted (clean) JSON payloads, one per line, to `/home/user/etl_output/clean.jsonl`.
   - Write rejected (evil/malformed/outlier) JSON payloads, one per line, to `/home/user/etl_output/rejected.jsonl`.
   - Ensure the JSON properties are preserved as closely as possible.

We have a test script that will run against your services. It will pump thousands of transactions through your Flask API. You must correctly configure the services, compile your C++ worker, start the worker process, and leave the pipeline running. Create a wrapper script at `/home/user/start_all.sh` that starts the Flask app, Redis, and your C++ worker in the background.