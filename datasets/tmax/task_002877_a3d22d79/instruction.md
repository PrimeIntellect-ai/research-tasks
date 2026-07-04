You are an MLOps engineer tasked with analyzing inference benchmark logs for two Large Language Models (Model A and Model B) to determine if Model B is significantly faster than Model A.

You have been provided with log files in the directory `/home/user/experiment_logs`. There are two files: `model_A.log` and `model_B.log`.

Each line in the log files represents a single inference run and has the following format:
`[TIMESTAMP] INFO: Inference complete. Model: {MODEL_NAME}, Input ID: {ID}, Latency: {LATENCY}ms, Output: {GENERATED_TEXT}`

Your task is to build a small ETL pipeline and run a statistical hypothesis test:
1. Parse the logs to extract the `Latency` (in milliseconds) and the `Output` text for each run.
2. Calculate the number of tokens in the `Output` text. For this task, a "token" is simply defined as a whitespace-separated word.
3. Compute the generation speed in Tokens Per Second (TPS) for each run. Formula: `TPS = token_count / (latency_ms / 1000)`.
4. Perform an independent two-sample Student's t-test (assume equal variances) comparing the TPS of Model B against Model A. Specifically, calculate the statistics for (Model B - Model A).
5. Calculate the 95% confidence interval for the difference in means (Mean TPS of B - Mean TPS of A).

Write a script in the language of your choice (Python is recommended) to perform this analysis.
Save the results in a JSON file at `/home/user/benchmark_results.json` with the exact following keys, rounding all float values to 4 decimal places:

```json
{
  "model_A_mean_tps": 0.0000,
  "model_B_mean_tps": 0.0000,
  "t_statistic": 0.0000,
  "p_value": 0.0000,
  "mean_diff_ci_lower": 0.0000,
  "mean_diff_ci_upper": 0.0000
}
```

Make sure your t-statistic represents `Model B - Model A` (so if B is faster, the t-statistic is positive). Use a two-sided test for the p-value.