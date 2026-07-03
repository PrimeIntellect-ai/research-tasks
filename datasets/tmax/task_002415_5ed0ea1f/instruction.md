You are an MLOps engineer auditing an old machine learning pipeline. We need to verify the reproducibility of a saved linear regression model artifact.

You have been provided with three files in the `/home/user` directory:
1. `/home/user/embeddings.csv`: A dataset of 100 samples and 3 features (matrix $X$).
2. `/home/user/targets.csv`: The continuous target values for the 100 samples (vector $Y$).
3. `/home/user/model_artifact.txt`: The saved model weights from a previous training run (3 comma-separated floats).

Your task is to write a Python script to perform the following reproducibility audit:
1. Load the embeddings and targets. Do **not** add a bias/intercept term.
2. Using pure linear algebra operations (e.g., `numpy`), compute the exact closed-form Ordinary Least Squares (OLS) regression weights: $W = (X^T X)^{-1} X^T Y$.
3. Load the artifact weights from `model_artifact.txt`.
4. Compute the Mean Squared Error (MSE) on the dataset using your computed OLS weights.
5. Compute the Mean Squared Error (MSE) on the dataset using the artifact weights.
6. Determine if the artifact is exactly reproducible. Consider it reproducible (`true`) if the absolute difference between the OLS MSE and the artifact MSE is less than `1e-5`. Otherwise, it is `false`.

Save your final audit results in a JSON file at `/home/user/audit_report.json`. The JSON must have the exact following schema, with all floats rounded to exactly 4 decimal places:

```json
{
  "ols_weights": [1.1111, 2.2222, 3.3333],
  "artifact_weights": [1.1111, 2.2222, 3.3333],
  "ols_mse": 0.1234,
  "artifact_mse": 0.5678,
  "reproducible": false
}
```

Ensure your Python script runs successfully and produces the required file.