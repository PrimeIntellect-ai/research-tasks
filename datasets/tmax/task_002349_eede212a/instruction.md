You are acting as a performance engineer analyzing the scaling characteristics of a newly deployed microservice. 

You have been provided with a dataset of performance profiling logs located at `/home/user/perf_logs.csv`. This CSV file contains three columns:
1. `concurrency`: The number of simultaneous requests.
2. `data_size_kb`: The payload size per request in kilobytes.
3. `latency_ms`: The measured response time in milliseconds.

Your task is to model the application's latency to predict future performance degradation. 

Theoretical analysis suggests the latency follows a non-linear interaction model:
`Latency(C, D) = a * C + b * D + c * C * D + d`
Where:
- `C` is concurrency
- `D` is data_size_kb
- `a`, `b`, `c`, and `d` are the hidden application parameters we need to discover.

Please perform the following steps:
1. **Data Cleaning:** Parse the CSV file and remove any data points where `latency_ms` is strictly greater than 9000 (these represent system timeouts and dropped connections, which skew the regression).
2. **Curve Fitting & Optimization:** Write a Python script to fit the remaining data to the theoretical model above, minimizing the sum of squared errors to find the optimal parameters for `a`, `b`, `c`, and `d`.
3. **Reporting:** Output the computed parameters to a JSON file located precisely at `/home/user/model_params.json`. 

The JSON file must have exactly this structure, with the numerical values rounded to exactly 4 decimal places:
```json
{
  "a": 0.0000,
  "b": 0.0000,
  "c": 0.0000,
  "d": 0.0000
}
```

You may use any standard data science libraries (e.g., `numpy`, `scipy`, `pandas`) available or install them via `pip`.