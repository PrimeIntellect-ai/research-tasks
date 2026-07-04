You are a performance engineer tasked with profiling a new microservice architecture. The environment consists of three components located in `/app/services/`:
1.  **Nginx (Reverse Proxy):** Configuration is in `/app/services/nginx/nginx.conf`. It should listen on port 8080 and forward traffic to the application server.
2.  **Application Server (FastAPI):** Code is in `/app/services/app/main.py`. It should run on port 8000. It depends on a Redis cache.
3.  **Redis Cache:** Needs to run on its default port (6379).

**Part 1: Service Composition**
Start and configure these services so that they communicate correctly.
-   Modify `/app/services/nginx/nginx.conf` to correctly proxy `http://127.0.0.1:8000`.
-   Modify `/app/services/app/.env` so the application connects to Redis at `127.0.0.1:6379`.
-   Ensure all three services are running in the background. A verification script will send HTTP GET requests to `http://127.0.0.1:8080/compute` and expect successful 200 OK responses containing valid JSON.

**Part 2: Profiling Data Analyzer**
You must write a log processing and density estimation script at `/home/user/analyzer.py`. This script will be used to profile the latencies.
It must accept a single command-line argument: a comma-separated string of integer latency values (e.g., `12,45,33,10,8`).
For each list of latencies, the script must:
1.  Filter out any values <= 0 or > 1000.
2.  Compute the standard Gaussian Kernel Density Estimate (KDE) evaluated exactly at the points `x = 10, 50, 100`. Use a fixed bandwidth of `h = 10.0`. 
    The KDE formula to use for a point `x` given `N` valid latencies `L_i` is:
    `KDE(x) = (1 / (N * h)) * SUM( (1 / sqrt(2 * pi)) * exp( -0.5 * ((x - L_i) / h)^2 ) )`
3.  Output the three KDE values as a comma-separated string, formatted to exactly 6 decimal places (e.g., `0.012345,0.000123,0.000000`), with no trailing newline or extra spaces.

Your `analyzer.py` must be completely self-contained (using only standard library functions for math, no `scipy` or `numpy`) and executable (`chmod +x /home/user/analyzer.py`). It must produce BIT-EXACT output matching our reference mathematical profiler.