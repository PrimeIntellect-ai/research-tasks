You are a data scientist working on a legacy system where only standard Unix core utilities (Bash, awk, sed, etc.) are permitted. You need to build a reproducible pipeline to clean a dataset of server logs, apply a simple Bayesian model to estimate true error rates, and output a sorted evaluation report.

We are modeling the probability of an error for each server using a Beta-Binomial conjugate model. 
- Prior distribution parameters: `alpha = 2` (prior errors), `beta = 10` (prior successes).
- Therefore, the posterior mean error rate for a server is given by: `(errors + alpha) / (requests + alpha + beta)`.

Your task is to create an executable Bash script at `/home/user/pipeline.sh` that performs the following end-to-end tasks:

1. **Data Cleaning**:
   Read the raw dataset at `/home/user/raw_logs.csv` (which has a header row: `server_id,requests,errors`).
   Filter out invalid rows based on the following rules:
   - Skip the header row in the output.
   - Remove rows with missing or non-numeric values in `requests` or `errors`.
   - Remove rows where `requests` is less than 1.
   - Remove rows where `errors` is less than 0.
   - Remove rows where `errors` is strictly greater than `requests`.

2. **Bayesian Inference & Model Evaluation**:
   For each valid row, calculate the posterior mean error rate using the formula provided above.
   Format the computed posterior mean to exactly 4 decimal places (e.g., 0.0625).

3. **Reporting & Pipeline Reproducibility**:
   Sort the final results by the posterior error rate in descending order. If there is a tie, sort by `server_id` in ascending alphabetical order.
   Save the final output to `/home/user/posteriors.csv` in the format `server_id,posterior_error_rate` (no header).

Ensure your script `/home/user/pipeline.sh` is fully self-contained, executable, and relies only on Bash and standard POSIX tools like `awk`, `sed`, `grep`, or `sort`. Execute your script to generate `/home/user/posteriors.csv`.