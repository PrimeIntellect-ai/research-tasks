You are a performance engineer analyzing the latency profiles of a distributed cache application. You have collected a set of latency histograms for two different application versions (Version A and Version B) across different simulated workload sizes. 

Your goal is to write a Rust program that analyzes this multi-dimensional performance data to determine how the latency distributions differ between versions, and to model the latency growth of Version B.

I have placed the raw data in `/home/user/latency_profiles.json`. The data format is:
```json
{
  "workload_sizes": [10.0, 20.0, 30.0, 40.0, 50.0],
  "bin_centers": [1.0, 2.0, 3.0, 4.0, 5.0],
  "version_a_histograms": [
    [0.2, 0.2, 0.2, 0.2, 0.2],
    [0.1, 0.2, 0.4, 0.2, 0.1],
    [0.05, 0.1, 0.2, 0.4, 0.25],
    [0.1, 0.1, 0.2, 0.3, 0.3],
    [0.2, 0.3, 0.3, 0.1, 0.1]
  ],
  "version_b_histograms": [
    [0.1, 0.2, 0.4, 0.2, 0.1],
    [0.05, 0.1, 0.2, 0.4, 0.25],
    [0.01, 0.04, 0.15, 0.4, 0.4],
    [0.0, 0.05, 0.1, 0.25, 0.6],
    [0.0, 0.0, 0.05, 0.15, 0.8]
  ]
}
```
*Note: Each array inside `version_a_histograms` and `version_b_histograms` corresponds to a workload size in `workload_sizes`, in the same order. The values are the normalized probabilities for the latency bins given in `bin_centers`.*

Write a Rust project in `/home/user/perf_analysis` that performs the following:

1. **Probability Distribution Distance:** Calculate the Jensen-Shannon (JS) divergence between the Version A and Version B histograms for *each* workload size. 
   * Use the natural logarithm ($\ln$) for the Kullback-Leibler (KL) divergence component.
   * If a probability is 0, treat $0 \ln(0)$ as 0.

2. **Array Manipulation & Expected Values:** For Version B only, calculate the expected latency (the mean) for each workload size. The expected value is the sum of `(probability * bin_center)` across all bins for a given histogram.

3. **Curve Fitting:** Perform a least-squares polynomial regression to fit a quadratic curve ($y = ax^2 + bx + c$) to the expected latencies of Version B. 
   * $x$ represents the `workload_sizes`.
   * $y$ represents the expected latencies calculated in step 2.
   * Calculate coefficients $a$, $b$, and $c$.

Finally, your Rust program must output the results to `/home/user/perf_report.json` exactly in this format:
```json
{
  "js_divergences": [
    <divergence_for_size_10>,
    <divergence_for_size_20>,
    <divergence_for_size_30>,
    <divergence_for_size_40>,
    <divergence_for_size_50>
  ],
  "version_b_expected_latencies": [
    <expected_latency_10>,
    ...
  ],
  "regression_coefficients": {
    "a": <a_value>,
    "b": <b_value>,
    "c": <c_value>
  }
}
```

Ensure the Rust program compiles and runs successfully, generating the file as requested. All float values in the JSON output should be standard IEEE 754 double precision.