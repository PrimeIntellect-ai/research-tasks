You are a performance engineer tasked with profiling a local multi-service application stack. The stack consists of a Web API, a Redis cache, and a background Worker process, located in `/app/`.

Currently, the services are not correctly communicating. 
1. Modify `/app/config.env` to properly link the services. The Web API needs to connect to the local Redis instance (running on the standard port 6379), and the Worker needs to listen to the Web API. Set the appropriate environment variables (`REDIS_HOST`, `REDIS_PORT`, `WEB_API_URL=http://127.0.0.1:5000`).
2. Once the configuration is fixed, start the stack using `/app/start_stack.sh`. 
3. Run the load test by executing `/app/run_load.sh`. This will hit the glued services and generate a multi-dimensional performance log at `/home/user/metrics.csv`. The CSV has four columns: `Time_s`, `Requests_Per_Sec`, `Latency_ms`, `CPU_util`.

Your main task is to write a Bash script at `/home/user/profile.sh` (which may invoke inline Python or a Python script you write) to analyze this multi-dimensional array of data and perform the following scientific computing operations:

A. **Numerical Integration**: Calculate the total CPU resources consumed by integrating the `CPU_util` curve over `Time_s` using the Trapezoidal rule.
B. **Numerical Differentiation**: Calculate the rate of change of latency over time. Find the maximum positive derivative (using forward finite difference) of `Latency_ms` with respect to `Time_s`.
C. **Curve Fitting / Regression**: Fit a 2nd-degree polynomial (quadratic) to model the relationship between load and latency: $Latency = a \cdot (Requests)^2 + b \cdot (Requests) + c$. Determine the coefficients $a, b, c$.

Your script `/home/user/profile.sh` must execute the analysis and generate a strict JSON file at `/home/user/analysis.json` with exactly these keys:
```json
{
  "total_cpu_integral": 0.0,
  "max_latency_derivative": 0.0,
  "poly_a": 0.0,
  "poly_b": 0.0,
  "poly_c": 0.0
}
```

The automated verifier will compute the exact mathematical solutions from your `metrics.csv` and compare them against your `analysis.json`. To pass, the absolute error for each metric must be less than 0.01.