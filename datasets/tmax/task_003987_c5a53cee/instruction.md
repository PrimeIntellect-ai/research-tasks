You are a FinOps analyst tasked with optimizing our cloud resource allocations to reduce costs while maintaining acceptable latency. We use a proprietary, black-box billing and latency engine provided as a binary.

Your goal is to build an automated pipeline that finds the optimal resource allocation for our API endpoints, generates the corresponding reverse proxy configuration, and deploys it.

Here are the requirements:

1. **The Oracle Binary**: 
   There is a stripped, compiled binary at `/app/pricing_oracle`. 
   Usage: `/app/pricing_oracle <request_rate> <allocation_units>`
   Output format: `Latency: <L> ms, Cost: $<C>`
   (Note: `allocation_units` must be an integer between 1 and 100).

2. **Traffic Data**:
   A CSV file at `/home/user/traffic.csv` contains our current traffic patterns with headers: `endpoint_path,request_rate`.

3. **C++ Optimizer & Config Generator**:
   Write a C++ program at `/home/user/optimizer.cpp` that reads `traffic.csv` and systematically queries the `/app/pricing_oracle` binary (by spawning it as a subprocess) to find the *minimum* `allocation_units` for each endpoint that keeps `Latency <= 200` ms.
   
   The C++ program must output:
   - A CSV file at `/home/user/optimal_allocations.csv` with headers: `endpoint_path,allocation_units,cost`
   - An Nginx configuration file at `/home/user/optimized_nginx.conf`. This config must:
     - Listen on port `8080`.
     - Define a `location` block for each `endpoint_path` that proxies requests to `http://127.0.0.1:9000`.
     - Include a custom access log format named `finops` that logs the request time, upstream response time, and the requested path. Log to `/home/user/logs/access.log`.

4. **Log Management**:
   Create a logrotate configuration file at `/home/user/logrotate.conf` to rotate the Nginx access log daily, keeping 7 days of logs, and compressing old ones.

5. **CI/CD Deployment Script**:
   Write a bash script at `/home/user/deploy.sh` that:
   - Compiles the C++ program (using `g++` with C++17).
   - Runs the compiled optimizer.
   - Starts or reloads Nginx using the generated `/home/user/optimized_nginx.conf`.
   - Ensure the script is executable.

To complete the task, execute `./deploy.sh` so that the final `optimal_allocations.csv` is generated and Nginx is running. We will evaluate your success based on the total cost achieved in your allocations file.