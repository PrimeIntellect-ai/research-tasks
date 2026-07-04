You are an MLOps engineer maintaining a model serving pipeline. A recent bug in an upstream pandas pipeline silently introduced `NaN` values into the latency fields of your inference logs. 

You need to track the performance of two model versions (`A` and `B`) currently running in production, but you must do this entirely using standard Linux command-line tools (like `awk`, `grep`, `sed`, `jq`, etc.) to generate a quick, automated tracking artifact.

You have a CSV log file at `/home/user/inference_logs.csv` with the following columns:
`timestamp,model_version,latency_ms`

Your task is to:
1. Parse the CSV file and filter out any rows where `latency_ms` is exactly `NaN` or a non-numeric string. Ignore the header.
2. For each `model_version` (`A` and `B`), calculate the sample mean and the 95% confidence interval for the mean latency.
    * Use the sample standard deviation formula (divided by $N-1$).
    * Calculate the Standard Error of the Mean (SEM) as $s / \sqrt{N}$.
    * Calculate the 95% Confidence Interval bounds using the approximation: $\mu \pm 1.96 \times SEM$.
3. Output the results to a tracking file at `/home/user/experiment_metrics.json`.

The JSON file must exactly match the following structure, with all numerical values rounded to exactly 2 decimal places (e.g., `108.80` instead of `108.8`):

```json
{
  "A": {
    "mean": "...",
    "ci_lower": "...",
    "ci_upper": "..."
  },
  "B": {
    "mean": "...",
    "ci_lower": "...",
    "ci_upper": "..."
  }
}
```

Ensure your tools handle the math correctly.