You are a data scientist and systems engineer tasked with fixing and completing a high-throughput, real-time data cleaning pipeline. 

We receive dirty sensor readings via a REST API. The system consists of four components:
1. **Nginx** (Reverse proxy, listening on port 8080)
2. **Flask API** (Receives data and queues it, running on port 5000)
3. **Redis** (Message queue, running on port 6379)
4. **C Worker** (Pulls data from Redis, cleans it, finds similarities, and logs it)

Currently, the services are provided in `/app/` but are misconfigured. The end-to-end flow is broken, and the C worker hasn't been implemented.

Your tasks are as follows:

### 1. Service Reconfiguration
- Start Redis.
- Fix the Nginx configuration located at `/app/nginx.conf` so it correctly forwards traffic from port 8080 to the Flask app on port 5000. Start Nginx using this config.
- Fix the Flask app (`/app/api.py`) so it correctly connects to Redis on localhost:6379 and pushes comma-separated strings to a Redis list called `sensor_queue`. Start the Flask app.

### 2. Implement the C Worker
Write a C program at `/home/user/worker.c` (you may use `hiredis` which is installed on the system, link with `-lhiredis`) that continuously pops items from the `sensor_queue` (using `BLPOP`). 

Each popped string has the format: `record_id,val1,val2,val3,val4,val5`.
Some values might be the string `"NaN"`, and some values might be extreme outliers.

For each record, the C worker must:
1. **Missing Value Handling:** Replace any `"NaN"` value with the mean of the *valid* numerical values in that specific record.
2. **Outlier Handling:** After missing value imputation, if any value is greater than `50.0`, clamp it exactly to `50.0`. If less than `-50.0`, clamp it to `-50.0`.
3. **Similarity Search:** Calculate the Euclidean distance between the cleaned 5-dimensional reading and a set of reference profiles provided in `/app/references.csv` (format: `ref_id,v1,v2,v3,v4,v5`). Find the `ref_id` of the closest reference profile.
4. **Model Output Validation:** Only accept the record if the Euclidean distance to the nearest reference profile is strictly less than `20.0`. 
5. If accepted, append the cleaned record to `/tmp/cleaned_output.csv` in the exact format: `record_id,val1,val2,val3,val4,val5,closest_ref_id`. (Print floats to 2 decimal places).

### 3. Execution
Compile your C program and run it in the background so it is ready to process incoming data.

Ensure all services (Nginx, Flask, Redis, and your C worker) are running. An automated test will fire thousands of HTTP POST requests to `http://localhost:8080/ingest` with JSON payloads like `{"payload": "123,1.0,NaN,55.0,-2.0,3.14"}`. 

Your C worker must process these in real-time and output the highly accurate cleaned dataset.