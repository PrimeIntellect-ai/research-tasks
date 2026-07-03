You are helping a researcher organize and validate their dataset pipelines. The researcher has run a Bayesian inference pipeline multiple times to estimate the bias of a coin using a Beta-Binomial conjugate model. However, they suspect some of the pipeline runs suffered from reproducibility issues or silent data corruption.

They have provided a CSV file at `/home/user/pipeline_runs.csv` containing the prior parameters, observed data, and the pipeline's estimated posterior mean and variance.

Your task is to validate these model outputs by analytically computing the true posterior mean and variance for each run, and comparing them against the pipeline's reported estimates. 

The Bayesian model is as follows:
- Prior distribution: Beta(alpha, beta)
- Observed data: `heads` (successes), `tails` (failures)
- Posterior distribution: Beta(A, B), where A = alpha + heads, and B = beta + tails.

The analytical formulas for the posterior are:
- True Mean = A / (A + B)
- True Variance = (A * B) / ( (A + B)^2 * (A + B + 1) )

A pipeline run is considered "PASSED" if both of the following are true:
1. The absolute difference between the pipeline's `estimated_mean` and the True Mean is less than or equal to 0.01.
2. The absolute difference between the pipeline's `estimated_variance` and the True Variance is less than or equal to 0.001.
Otherwise, it is considered "FAILED".

Using standard shell utilities (e.g., `awk`, `sed`, `bash`), create a CSV report at `/home/user/validation_report.csv` with exactly two columns: `run_id` and `status`. The first line must be the header `run_id,status`, followed by each run ID and its evaluation result (`PASSED` or `FAILED`).

Ensure your output is strictly formatted and correctly sorted by `run_id`.