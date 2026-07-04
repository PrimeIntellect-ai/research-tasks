You are a performance engineer tasked with profiling an application's API latency before and after a major caching patch. You have been provided with two files containing latency measurements (in milliseconds):
- `/home/user/latency_v1.csv` (Baseline measurements)
- `/home/user/latency_v2.csv` (Post-patch measurements)

Both files contain a single column of floating-point numbers with no header.

Your task is to statistically analyze the change in the latency distributions by following these exact steps:

1. **Environment Management:** Create a Python virtual environment at `/home/user/perf_env`. Activate it and install `numpy` and `scipy`. All your analysis must be run using this environment.

2. **Statistical Analysis:** Write a Python script at `/home/user/analyze_perf.py` that reads the two CSV files and calculates two metrics:
   - The **Wasserstein distance** (Earth Mover's Distance) between the `v1` and `v2` empirical distributions to quantify the magnitude of the shift.
   - The p-value from a **2-sample Kolmogorov-Smirnov (KS) test** (comparing `v1` against `v2`) to test the null hypothesis that both sets of latencies are drawn from the same underlying distribution.

3. **Report Generation:** Your script must write a JSON file to `/home/user/perf_report.json` with exactly the following format (round the values to 4 decimal places):
```json
{
    "wasserstein_distance": <float>,
    "ks_p_value": <float>
}
```

Do not use any external tools or APIs other than `numpy` and `scipy`. Your script should be entirely self-contained and execute cleanly.