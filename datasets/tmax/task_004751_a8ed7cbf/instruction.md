I need you to deploy and complete a real-time CSV anomaly detection pipeline. We have a multi-service architecture located in `/home/user/pipeline/` consisting of an Nginx reverse proxy, a Flask ingestion API, and a Redis message queue. 

Your objective is to complete the pipeline by writing a high-performance C++ worker (`/home/user/worker/sanitizer.cpp`) that reads CSV records from the Redis queue, applies a mathematical classification to detect "evil" (anomalous) data, and outputs the filtered results. You will also need to reconfigure the services to establish the correct end-to-end flow.

Here are the specific requirements:

1. **Service Configuration (Multi-Service Compose):**
   - The services are defined in `/home/user/pipeline/docker-compose.yml`. 
   - Nginx is listening on port 8080. It must be configured to route requests from `/api/ingest` to the Flask service on port 5000. Edit `/home/user/pipeline/nginx/nginx.conf` to fix the missing upstream route.
   - The Flask app (`/home/user/pipeline/flask/app.py`) parses incoming CSV payloads and pushes them to a Redis list named `raw_csv_queue`. Edit the Flask app so it correctly connects to the Redis service (hostname: `redis`, port: 6379).
   - Start the services using `docker-compose up -d`. (Note: docker and docker-compose are already installed).

2. **C++ Sanitization Worker (Adversarial Corpus):**
   - Write a C++ program at `/home/user/worker/sanitizer.cpp`.
   - The program must connect to Redis (using `hiredis`, which you should install/link) and continuously `BLPOP` from `raw_csv_queue`.
   - Each popped message is a comma-separated string containing a batch ID, a feature ID, and 10 floating-point sensor readings: `batch_id,feature_id,val1,val2,...,val10`.
   - **Multi-source joining:** The worker must load reference statistics from `/home/user/data/reference_stats.csv` (contains `feature_id, mean, stddev`).
   - **Hypothesis Testing & Classification:** For each message, calculate the sample mean of the 10 sensor readings. Perform a one-sample Z-test against the reference mean and standard deviation for that `feature_id`. 
   - Reject the batch (classify as "evil") if the two-tailed p-value is less than 0.01 (or equivalently, if the absolute Z-score is > 2.576). 
   - Accept the batch (classify as "clean") otherwise.
   - **Performance Benchmarking:** Track the total inference time (in microseconds) for processing each payload.
   - The program must append accepted (clean) payloads to `/home/user/worker/clean_output.csv` and rejected (evil) payloads to `/home/user/worker/evil_output.csv`. The format for these files must be: `batch_id,feature_id,z_score,inference_time_us`.

3. **End-to-End Execution:**
   - Once your worker is compiled and running, a background grading script will inject a stream of adversarial payloads (both clean and evil) through the Nginx endpoint at `http://localhost:8080/api/ingest`.
   - You can simulate this yourself by sending POST requests with raw CSV data to that endpoint.
   - Leave your C++ worker running and output a log file `/home/user/worker/run.log` indicating "WORKER READY" when it is actively polling Redis.

Please ensure your C++ code is robust and your service configurations are exact. The automated verification will inspect the final output files to ensure 100% of the evil corpus was rejected and 100% of the clean corpus was accepted.