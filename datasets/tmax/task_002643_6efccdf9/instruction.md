You are an SRE investigating a broken monitoring stack for our microservices. The stack consists of a Go-based dependency health checker and a Python-based metrics dashboard. Both are currently failing to run or returning incorrect data.

Your goal is to fix the bugs, recover missing credentials, and bring the monitoring dashboard online on port 8080.

Here is what you need to do:

1. **Extract Authentication Requirements:**
   We received an alert screenshot located at `/app/alert_config.png`. You must extract the `AuthToken` visible in this image. The Python dashboard must be configured to require this token in the `Authorization: Bearer <token>` header for all incoming requests.

2. **Git Forensics for the State Key:**
   The Go health checker (`/home/user/monitor-stack/checker/`) reads a local binary state file (`/home/user/monitor-stack/state.dat`). However, it requires a decryption key that was accidentally deleted from the repository. Search the Git history of the `monitor-stack` repository to find the deleted `STATE_KEY` and set it as an environment variable when running the Go checker.

3. **Fix the Infinite Recursion (Go):**
   The Go checker has a function that recursively resolves service dependencies to determine overall health. Recently, a cyclic dependency was introduced in our infrastructure mock, causing the Go checker to crash with a stack overflow. Modify the Go code to properly handle cyclic dependencies (e.g., by tracking visited nodes) and terminate the loop gracefully, returning a healthy state for cycles.

4. **Fix Numerical Instability (Python):**
   The Python dashboard (`/home/user/monitor-stack/dashboard/app.py`) calculates the variance and standard deviation of service response times. It currently crashes due to a `ValueError: math domain error` (taking the square root of a negative number) because it uses a naive variance formula (`E[X^2] - (E[X])^2`) that suffers from floating-point catastrophic cancellation. 
   Rewrite the variance calculation to use a numerically stable method (like Welford's algorithm or a two-pass mean-centered approach). Trace the intermediate state and write the corrected variance for the `db-service` to `/home/user/variance_debug.txt`.

5. **Start the Services:**
   Compile and run the Go checker (it writes health data to `/tmp/health.json`).
   Start the Python dashboard (it reads `/tmp/health.json` and exposes it).
   The Python dashboard MUST listen on `127.0.0.1:8080`.
   It must expose the endpoint `GET /api/status`.
   
When the verifier checks your work, it will send an HTTP GET request to `http://127.0.0.1:8080/api/status` using the `AuthToken` from the image. Ensure the service is running and properly authenticated before you finish.