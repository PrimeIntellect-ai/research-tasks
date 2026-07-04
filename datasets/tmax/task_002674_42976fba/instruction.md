You are a Machine Learning Engineer preparing a robust data pipeline to filter out poisoned or anomalous sensor readings before they are used for model training. 

We have a multi-service pipeline that ingests sensor data, but it is currently broken and lacking the core Bayesian filtering logic. The system uses Nginx, a Python Flask API, Redis, and a C++ worker.

Your objectives:

1. **Service Configuration (Multi-Service Compose)**
   A startup script at `/app/start_services.sh` brings up Redis (port 6379) and the Python API (port 5000). 
   There is an Nginx configuration file at `/home/user/nginx.conf`. It is supposed to run in user-space, listening on port 8080, and routing requests for `/api/` to the Python API. However, the configuration is incomplete/incorrect. Fix `/home/user/nginx.conf` and start Nginx using `nginx -c /home/user/nginx.conf`. 
   
2. **Implement the Bayesian Filter (C++)**
   The Python API pushes incoming sensor data as JSON strings to a Redis list called `incoming_queue`.
   You must implement a C++ worker that continuously pops items from `incoming_queue` (using `BLPOP`), evaluates them using a Bayesian probabilistic model, and pushes the result to `processed_queue`.
   
   The sensor data JSON looks like: `{"id": "item_123", "a": 48.2, "b": 105.1, "c": 108.3}`.
   
   **Clean Data Distribution Model:**
   - Feature `a` is normally distributed: mean = 50.0, std = 5.0
   - Feature `b` is normally distributed: mean = 100.0, std = 10.0
   - Feature `c` depends on `a` and `b`: `c = 0.5 * a + 0.8 * b + noise`, where `noise` is normally distributed with mean = 0.0, std = 2.0.
   - `a` and `b` are independent.
   
   Your C++ worker must calculate the joint log-likelihood of `(a, b, c)`. If the log-likelihood falls below a certain threshold (you must determine an appropriate threshold to perfectly separate clean and evil data), it should be classified as "REJECT", otherwise "CLEAN".
   
   The worker must push a JSON string to `processed_queue` in the format: `{"id": "item_123", "status": "CLEAN"}` or `{"id": "item_123", "status": "REJECT"}`.

3. **Verify against the Adversarial Corpus**
   We have provided two corpora of raw JSON payloads:
   - Clean data: `/app/data/clean/`
   - Poisoned data: `/app/data/evil/`
   
   You must ensure your C++ program and pipeline correctly process these. The test suite will send all files from both directories through the Nginx endpoint `http://127.0.0.1:8080/api/ingest`, and then check the `processed_queue` in Redis. 
   **Pass Requirement:** 100% of clean data must be classified as "CLEAN", and 100% of evil data must be classified as "REJECT".

Compile your C++ worker to `/home/user/filter_worker` and leave it running in the background. You can use `hiredis` (already installed) and a JSON library of your choice (e.g., `nlohmann-json3-dev` is installed). Make sure Nginx, Redis, the Flask API, and your C++ worker are all running and communicating correctly.