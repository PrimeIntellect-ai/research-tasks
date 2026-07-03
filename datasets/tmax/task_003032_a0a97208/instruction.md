You are a performance engineer tasked with profiling a new microservice architecture. The system consists of three components that currently fail to communicate due to misconfiguration. After fixing the application, you must implement a standalone metrics analyzer in Bash.

Part 1: Service Configuration
The application resides in `/app/perf_env/`. It consists of:
1. A Redis cache backend.
2. A Flask API (which is supposed to read metrics from Redis).
3. A Load Generator (which hits the Flask API).

Currently, the startup script `/app/perf_env/start_services.sh` fails because the service ports and environment variables in `/app/perf_env/config.env` are misaligned. 
- Redis should run on port `6380` (as configured in its local `redis.conf`).
- The Flask API must be told to connect to Redis on port `6380` and listen on port `5000`.
- The Load Generator must target `http://127.0.0.1:5000`.
Modify `/app/perf_env/config.env` so that all three services start correctly and the Load Generator reports "Flow Complete" in `/home/user/load_gen.log`.

Part 2: Metrics Analysis Script
The Load Generator produces simulated CPU load (x) and Latency (y) pairs. We need to fit a line to these metrics to predict tail latency, and calculate the variance of the residuals to estimate the density of the latency distribution.

Create a Bash script at `/home/user/analyze_metrics.sh`. It must accept exactly 10 floating-point arguments representing 5 pairs of `x y` data points.
Example invocation:
`/home/user/analyze_metrics.sh 1.0 2.1 2.0 4.0 3.0 6.2 4.0 8.0 5.0 9.9`

The script must perform Ordinary Least Squares linear regression to find the line of best fit `y = mx + c` that minimizes the mean squared error (optimization of the residual sum of squares).
It must also compute the variance of the residuals (population variance, dividing by N=5).

The script must print exactly one line to stdout in this precise format (floats rounded to exactly 4 decimal places):
`Slope: 1.9700, Intercept: 0.1100, ResidualVar: 0.0104`

Your Bash script will be tested against a hidden, compiled oracle using fuzz testing. It must produce identical output for any 5 pairs of positive floating-point numbers between 0.0 and 100.0. You may use `awk` or `bc` inside your Bash script to perform the floating-point math. Ensure your script has executable permissions (`chmod +x`).