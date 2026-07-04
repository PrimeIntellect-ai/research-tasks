You are an AI assistant helping a data engineer debug an ETL pipeline validation step. 

We have a Python script located at `/home/user/etl_validation.py` that is supposed to read a dataset (`/home/user/data.csv`), perform statistical validation, and train a baseline model to check data quality. However, the script is currently failing or producing incorrect results.

Specifically, the pipeline is suffering from the following issues:
1. It is missing necessary Python dependencies to run.
2. The script attempts to generate a plot (`/home/user/bootstrap_dist.png`), but it crashes or produces a blank plot because it is running in a headless Linux environment and the plotting backend is misconfigured.
3. The bootstrap sampling implementation contains a logical error, causing the numerical accuracy testing to fail. The confidence intervals being generated do not reflect true bootstrap estimates.

Your task:
1. Install any necessary dependencies.
2. Fix the plotting issue in `/home/user/etl_validation.py` so that it successfully saves a valid histogram to `/home/user/bootstrap_dist.png` without requiring a GUI.
3. Fix the statistical bug in the bootstrap sampling logic. The bootstrap must properly sample the `target` column to estimate the mean and 95% confidence interval using 1000 iterations.
4. Ensure the script successfully runs and outputs the computed metrics to `/home/user/metrics.json`.

The final `metrics.json` file must contain exactly the following keys:
- `"bootstrap_mean"`: The mean of the bootstrap sample means.
- `"ci_lower"`: The 2.5th percentile of the bootstrap means.
- `"ci_upper"`: The 97.5th percentile of the bootstrap means.
- `"model_mse"`: The mean squared error of the linear regression model trained on the data.

Do not change the random seeds (`np.random.seed(42)`) in the script, as they are required for automated verification of the numerical accuracy.