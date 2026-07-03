You are a data scientist working on optimizing a high-throughput backend system. The engineering team has deployed two different load balancing algorithms (Algorithm 'A' and Algorithm 'B') and collected server response time data over a 24-hour period.

Your task is to build a reproducible computation pipeline to analyze the tail latencies, compare the two algorithms statistically, and generate a visualization. 

The raw data is located at `/home/user/server_metrics.csv` and contains two columns:
- `algorithm`: A string, either "A" or "B".
- `latency_ms`: A float representing the server response time in milliseconds.

Please perform the following steps:
1. **Dependency Management**: Install any required libraries (e.g., pandas, numpy, scipy, matplotlib if you choose Python).
2. **Point Estimates**: Calculate the empirical 95th percentile latency for both Algorithm A and Algorithm B.
3. **Bootstrap Confidence Intervals**: Compute the 95% Bootstrap Confidence Interval for the 95th percentile for each algorithm. 
   - You must use exactly 10,000 bootstrap resamples (sample with replacement).
   - Use a random seed of `42` for the random number generator before starting the resampling for Algorithm A, and reset the seed to `42` before resampling for Algorithm B. (If using Python, use `np.random.seed(42)`).
   - Use the percentile method (2.5th and 97.5th percentiles of the bootstrap distribution) to determine the lower and upper bounds.
4. **Statistical Hypothesis Comparison**: Perform a two-sided Mann-Whitney U test to determine if the underlying latency distributions of Algorithm A and Algorithm B are statistically different.
5. **Visualization**: Create an overlapping histogram (or KDE plot) of the latencies for A and B. Save this plot to `/home/user/latency_plot.png`.
6. **Reporting**: Create a JSON log file at `/home/user/analysis_results.json` with the exact following structure and your computed numeric values:

```json
{
  "algo_A": {
    "95th_percentile": 0.0,
    "ci_lower": 0.0,
    "ci_upper": 0.0
  },
  "algo_B": {
    "95th_percentile": 0.0,
    "ci_lower": 0.0,
    "ci_upper": 0.0
  },
  "mann_whitney_p_value": 0.0
}
```

Ensure your JSON file is properly formatted. Your script must be entirely reproducible.