You are acting as an assistant for a systems researcher organizing datasets and analyzing server performance. 

The researcher has collected system metrics from two different server configurations (Config A and Config B) and saved them in a CSV file located at `/home/user/system_metrics.csv`. 

Your task is to write a reproducible data science pipeline in **Rust** that parses this dataset, engineers a new feature, performs a statistical hypothesis test, and calculates a correlation.

**Dataset Format (`/home/user/system_metrics.csv`):**
The CSV has headers and contains the following columns:
`config` (String: "A" or "B"), `cpu_util` (Float), `mem_util` (Float), `latency_ms` (Float).

**Task Requirements:**
1. Initialize a Rust project in `/home/user/performance_analysis`.
2. Write a Rust program that reads the CSV file.
3. Calculate the **Mean `latency_ms`** for Config A and Config B separately.
4. Perform a **Welch's t-test** (two-tailed) comparing the `latency_ms` between Config A and Config B. Calculate the t-statistic and the p-value.
5. Engineer a new feature for all rows called `resource_pressure`, defined as: `cpu_util * mem_util`.
6. Calculate the **Pearson correlation coefficient** between the engineered `resource_pressure` and `latency_ms` across the *entire* dataset.
7. Output the results to a JSON file located at `/home/user/analysis_results.json`.

**Output Format (`/home/user/analysis_results.json`):**
The JSON file must have exactly this structure (using standard floating-point numbers):
```json
{
  "mean_latency_A": 120.0,
  "mean_latency_B": 90.0,
  "t_stat": 6.0,
  "p_value": 0.000318,
  "correlation": 0.95
}
```
*(Note: The values above are examples. Your program must compute the actual values based on the dataset. Precision up to 4 decimal places is acceptable for verification, though raw floats are fine).*

You may use standard Rust ecosystem crates like `csv`, `serde`, `serde_json`, and `statrs`.
Execute your Rust pipeline to generate the final JSON file.