You are assisting a scientific researcher who is building a reproducible computation pipeline for analyzing noisy simulation data. They are currently facing two main issues: a broken microservice pipeline for data ingestion, and numerical instability in their statistical routines (catastrophic cancellation when computing variance on large floating-point datasets).

Your objective has two parts:

### Part 1: Service Configuration (Pipeline Setup)
The data ingestion pipeline consists of three components located in `/app/pipeline/`:
1. **Redis**: Needs to be running on the default port (6379).
2. **Data API**: A Flask application (`api.py`) that accepts POST requests. It is configured to run on port 5000.
3. **Nginx**: Should act as a reverse proxy, listening on port 8080 and forwarding requests to the Data API.

However, the configuration is currently disconnected. 
- You must create or modify the Nginx configuration at `/app/pipeline/nginx.conf` so that any HTTP request to `http://localhost:8080/` is proxied to `http://127.0.0.1:5000/`.
- Start Redis, the Flask API, and Nginx using the provided `start_pipeline.sh` script (you may need to modify it to ensure all services start correctly and bind to the right ports).
- Verify the pipeline works: sending a POST request to `http://localhost:8080/data` with a JSON payload `{"value": 42.0}` should return a 200 OK and store it in Redis.

### Part 2: Stable Variance Computation
The researcher has an oracle binary at `/app/oracle_stat` that correctly computes the sample mean and sample variance of a dataset using **Welford's online algorithm** to prevent floating-point catastrophic cancellation. 

You must write a program at `/home/user/stable_stat` (you may use Python, C, C++, or any language of your choice, but it must be executable via `./stable_stat <input_file>`). 
This program must read a text file where each line contains a single floating-point number.
It must compute the sample mean and sample variance using strictly Welford's algorithm in double-precision (64-bit float) to ensure bit-exact equivalence with the oracle.

**Welford's Algorithm Specification:**
- Initialize `count = 0`, `mean = 0.0`, `M2 = 0.0`
- For each number `x`:
    - `count += 1`
    - `delta = x - mean`
    - `mean += delta / count`
    - `delta2 = x - mean`
    - `M2 += delta * delta2`
- `variance = M2 / (count - 1)` (if count < 2, variance is 0.0)

**Output Format:**
Your program must print exactly one line to standard output:
`Mean: <mean>, Variance: <variance>`
Format both numbers to exactly 8 decimal places.

We will test your `/home/user/stable_stat` program with an automated fuzzer that generates random floating-point datasets and compares your output bit-for-bit against `/app/oracle_stat`.