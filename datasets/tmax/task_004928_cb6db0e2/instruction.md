You are an MLOps engineer tasked with tracking and summarizing experiment artifacts using a suite of Bash tools. 

We have a vendored third-party data processing package located at `/app/bash-ops-etl-0.1.0`. It contains a script `bin/extract_valid_metrics.sh` intended to filter out failed runs and missing values from CSV logs. 

There are 50 raw experiment logs located in `/home/user/data/raw_logs/` (named `exp_01.csv` to `exp_50.csv`). Each CSV has the schema:
`experiment_id,run_status,val_loss`

Your task:
1. **Fix the Toolkit**: The `extract_valid_metrics.sh` script in the vendored package has a bug. It uses an `awk` condition that silently drops valid data (specifically, it drops rows where `val_loss` is exactly `0.0` by mistakenly evaluating the string "0.0" or integer `0` as falsy in its check for missing values). Find and fix this perturbation so that rows with `val_loss=0.0` are retained, while true empty values are dropped.
2. **Build the ETL Pipeline**: Write a Bash script `/home/user/run_etl.sh` that iterates over all CSVs in `/home/user/data/raw_logs/`, uses the fixed `/app/bash-ops-etl-0.1.0/bin/extract_valid_metrics.sh` to extract valid `val_loss` values for runs where `run_status` is `SUCCESS`.
3. **Probabilistic Modeling**: Instead of just averaging the losses, we want to perform a Bayesian update to find the posterior mean of the `val_loss`. 
   Assume:
   - Prior mean (\(\mu_0\)) = 0.5
   - Prior variance (\(\sigma_0^2\)) = 0.1
   - Known likelihood variance (\(\sigma^2\)) = 0.05
   - Data: The collection of extracted `val_loss` values (\(x_1, x_2, ..., x_n\))

   Using `awk` or `bc` within your pipeline, calculate the posterior mean using the conjugate normal-normal model formulas:
   - Posterior variance: \( \sigma_{post}^2 = \frac{1}{\frac{1}{\sigma_0^2} + \frac{n}{\sigma^2}} \)
   - Posterior mean: \( \mu_{post} = \sigma_{post}^2 \times \left( \frac{\mu_0}{\sigma_0^2} + \frac{\sum x_i}{\sigma^2} \right) \)

4. **Reporting**: Your script must output the final calculated posterior mean (as a float) into the file `/home/user/posterior_mean.txt`.

Ensure your script is executable and run it to generate the final output.