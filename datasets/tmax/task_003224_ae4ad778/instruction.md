You are an MLOps engineer tasked with fixing a bug in an existing machine learning script and implementing proper artifact tracking.

We have a script located at `/home/user/evaluate_model.py` that evaluates a Logistic Regression model. However, there is a "data leakage" bug: the data is being scaled before being split for cross-validation, which inflates the performance metric. Additionally, the evaluation is currently a single run of 5-fold CV, which doesn't give us a good confidence interval, and it doesn't log the results.

Your task is to modify `/home/user/evaluate_model.py` to do the following:

1. **Fix the Data Leakage**: Use `sklearn.pipeline.Pipeline` or `make_pipeline` to combine the `StandardScaler` and `LogisticRegression` (with `random_state=42`) so that scaling is strictly computed on the training folds and applied to the validation folds.
2. **Robust Evaluation**: 
   - Instead of a single cross-validation run, perform 50 iterations of 5-fold cross-validation. 
   - Use `StratifiedKFold(n_splits=5, shuffle=True, random_state=i)` where `i` iterates from `0` to `49` inclusive. 
   - Collect all 250 accuracy scores from these runs.
3. **Bootstrap Confidence Interval**: 
   - Compute the overall mean of the 250 scores.
   - Use the empirical bootstrap method to compute the 95% confidence interval of the **mean** score. 
   - Specifically, generate 1000 bootstrap samples (each of size 250, drawn with replacement from your 250 scores). Use `numpy.random.seed(42)` immediately before your bootstrap loop.
   - Calculate the mean of each bootstrap sample.
   - Find the 2.5th and 97.5th percentiles of these 1000 bootstrap means to determine the lower and upper bounds of the 95% confidence interval (use `numpy.percentile`).
4. **Artifact Tracking**: 
   - Create the directory `/home/user/artifacts` if it doesn't exist.
   - Save the results as a JSON file at `/home/user/artifacts/run_metrics.json`.
   - The JSON file must have exactly these keys: `"mean_accuracy"`, `"ci_lower"`, `"ci_upper"`, corresponding to the overall mean of the 250 scores, the bootstrap 2.5th percentile, and the bootstrap 97.5th percentile.

Ensure that the script runs successfully and writes the JSON file when executed.