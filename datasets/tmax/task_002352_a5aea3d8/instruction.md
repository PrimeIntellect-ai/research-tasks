You are an MLOps engineer evaluating two models (`model_alpha` and `model_beta`) based on raw prediction artifacts logged during an A/B test. The raw logs are messy and need processing, storage optimization, and rigorous statistical analysis.

Your tasks are:

1. **Environment Setup**: Ensure necessary Python libraries (like `pandas`, `pyarrow`, `scipy`, `numpy`) are installed.
2. **Schema Enforcement & Storage Management**:
   - Read the raw CSV logs at `/home/user/artifacts/raw_logs.csv`.
   - Enforce the following schema: `req_id` (string), `model` (string), `y_pred` (integer), `y_true` (integer).
   - Filter out any invalid rows (e.g., missing values, or where `y_pred`/`y_true` are strings like "ERROR" that cannot be cast to integers).
   - Save the cleaned dataset as a Parquet file at `/home/user/artifacts/cleaned_logs.parquet` to optimize for large-scale storage.
3. **Bayesian Inference**:
   - We want to model the accuracy (where `y_pred == y_true` is a success) of each model.
   - Using a **Beta(2, 2)** prior for both models, perform a conjugate Bayesian update using the cleaned dataset to find the posterior Beta distribution parameters for both models.
   - Save the posterior parameters to `/home/user/artifacts/posteriors.json` strictly in this format:
     ```json
     {
       "model_alpha": {"alpha": <int>, "beta": <int>},
       "model_beta": {"alpha": <int>, "beta": <int>}
     }
     ```
4. **Bootstrap Confidence Intervals**:
   - Write and execute a script to calculate the 95% confidence interval for the difference in accuracy (`accuracy_beta - accuracy_alpha`) using bootstrapping.
   - Setup: Use `numpy.random.seed(123)` immediately before generating your resamples.
   - Procedure: Generate exactly 10,000 bootstrap resamples (sampling the cleaned dataset with replacement, maintaining the original dataset size per resample). For each resample, calculate the difference in accuracy.
   - Calculate the 2.5th and 97.5th percentiles of these differences using `numpy.percentile` (default settings).
   - Save the confidence interval to `/home/user/artifacts/bootstrap_ci.txt` in the format `lower,upper`, with both numbers rounded to exactly 4 decimal places (e.g., `0.0123,0.0567`).