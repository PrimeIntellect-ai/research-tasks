You are an MLOps engineer tasked with processing experiment artifacts from a distributed model evaluation cluster. The raw logs contain experiment results, but they are notoriously messy due to sensor failures, missing logs, and zombie processes. 

You need to build a robust ETL pipeline in **Bash** to clean these logs and perform basic Bayesian inference to estimate the true success rate of each model.

The raw log file is located at `/home/user/raw_experiments.log`. 
It is a pipe-delimited (`|`) file with the following columns:
`experiment_id|model_name|successes|trials|exec_time_sec`

Write a Bash script at `/home/user/process_artifacts.sh` that processes this file using standard Linux command-line tools (e.g., `awk`, `sed`, `grep`, `bc`). Do not use Python, Ruby, or Perl.

Your pipeline must perform the following steps:
1. **Outlier Filtering:** 
   - Drop any row where `exec_time_sec` is strictly less than `0` or strictly greater than `3600`.
   - Drop any row where `successes` is greater than `trials` (after handling missing `trials` as described below).
2. **Missing Value Handling:**
   - If the `successes` field is empty, drop the row completely.
   - If the `trials` field is empty, impute its value as `1000`.
3. **Bayesian Inference:**
   - We want to model the success rate of each model using a Beta-Binomial conjugate prior.
   - Start with a uniform prior for all models: $\alpha_{prior} = 1$, $\beta_{prior} = 1$.
   - For each valid row, update the posterior parameters for that specific `model_name`:
     - $\alpha_{post} = \alpha_{prior} + \sum successes$
     - $\beta_{post} = \beta_{prior} + \sum (trials - successes)$
4. **Reporting:**
   - Calculate the expected value of the posterior distribution for each model: $E[\theta] = \alpha_{post} / (\alpha_{post} + \beta_{post})$.
   - Output the results to `/home/user/posterior_metrics.csv`.
   - The output must be comma-separated and contain a header: `model_name,alpha,beta,expected_value`.
   - Round `expected_value` to exactly 4 decimal places (e.g., `0.8497`).
   - Sort the output rows alphabetically by `model_name`.
   - Only include models that had at least one valid row after filtering.

Make sure your script `/home/user/process_artifacts.sh` has executable permissions and produces the exact specified output when run. You can create the script, test it, and run it to generate `/home/user/posterior_metrics.csv`.