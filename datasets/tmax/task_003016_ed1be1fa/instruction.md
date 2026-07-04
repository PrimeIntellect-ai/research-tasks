You are an MLOps engineer tracking experiment artifacts and inference benchmarking results. 

Your task is to write a Rust program that analyzes a set of model artifacts and inference benchmark logs, applying a simple Bayesian update to estimate the true inference latency, and summarizing the token count and storage usage.

The environment has been set up with:
1. A directory containing model artifacts: `/home/user/model_artifacts/`
2. A CSV file containing inference benchmark logs: `/home/user/inference_benchmarks.csv`. The CSV has two columns: `text_sample` and `latency_ms`.
3. A skeleton Rust project at `/home/user/mlops_tracker/`.

Write a Rust program in `/home/user/mlops_tracker/src/main.rs` that performs the following steps:

1. **Storage Management:** Calculate the total size in bytes of all files within `/home/user/model_artifacts/`.
2. **Tokenization Prep:** Read `/home/user/inference_benchmarks.csv` (skipping the header). "Tokenize" the `text_sample` column by splitting the text by ASCII whitespace, and calculate the total number of tokens across all rows.
3. **Bayesian Inference:** We want to estimate the true mean latency. Assume a Normal conjugate prior model for the mean latency:
   - Prior mean ($\mu_0$) = 50.0
   - Prior variance ($\sigma_0^2$) = 100.0
   - Likelihood (Observation) variance ($\sigma^2$) = 25.0
   - Number of observations ($n$) = total number of rows in the CSV
   - Sample mean ($\bar{x}$) = average of `latency_ms` column
   Calculate the posterior mean ($\mu_n$) using the standard conjugate update formula:
   $1 / \sigma_n^2 = (1 / \sigma_0^2) + (n / \sigma^2)$
   $\mu_n = \sigma_n^2 \times ( (\mu_0 / \sigma_0^2) + (n \bar{x} / \sigma^2) )$

4. **Reporting:** The program must create a JSON file at `/home/user/experiment_summary.json` with exactly the following structure:
```json
{
  "total_artifact_bytes": 12345,
  "total_tokens": 123,
  "posterior_mean_latency": 45.67
}
```
*Note: `posterior_mean_latency` should be rounded to 2 decimal places.*

You may modify `/home/user/mlops_tracker/Cargo.toml` if you wish to use external crates (like `csv` or `serde_json`), but standard library solutions are also acceptable. Once the code is written, compile and run it to produce the `experiment_summary.json` file.