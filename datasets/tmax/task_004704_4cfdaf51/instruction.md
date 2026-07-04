You are an MLOps engineer debugging a machine learning pipeline that has artificially inflated performance due to data leakage.

You have been provided with an initial script at `/home/user/src/experiment.py` and a dataset at `/home/user/data/dataset.csv`. The script currently loads the data, scales it, splits it, and trains a Ridge regression model. However, there is a data leakage problem: the standard scaling is applied to the entire dataset before the train-test split. 

Your tasks are:
1. **Fix the Data Leak:** Modify `/home/user/src/experiment.py` so that data transformations (like scaling) are applied correctly. You should use a `sklearn.pipeline.Pipeline` or fit the scaler only on the training data and transform the test data.
2. **Correlation-based Feature Selection:** Before passing data to the model, add a step (or write custom logic before training) that removes highly correlated features. Specifically, calculate the Pearson correlation matrix on the *training data only*. If any two features have an absolute correlation > 0.85, drop the one that appears later in the column order.
3. **Bootstrap Validation:** Instead of a single evaluation, implement a bootstrap validation loop. Create 100 bootstrap samples (sample with replacement, same size as the original training set) from the training data. For each sample, fit the pipeline (feature selection, scaling, Ridge model) and evaluate it on the single, untouched test set. Use a random seed from 0 to 99 for each respective bootstrap iteration (`random_state=i` for `i` in `range(100)`).
4. **Artifact Tracking:** Calculate the mean, 2.5th percentile (lower CI), and 97.5th percentile (upper CI) of the Mean Squared Error (MSE) across the 100 evaluations.
   Save these metrics to `/home/user/artifacts/metrics.json` in the exact format:
   `{"mean_mse": <float>, "ci_lower": <float>, "ci_upper": <float>}`
   Save the final pipeline (trained on the full, un-bootstrapped training set) to `/home/user/artifacts/pipeline.pkl` using `joblib`.

Requirements:
- Ensure the `train_test_split` uses `test_size=0.2` and `random_state=42`.
- `Ridge` should use default parameters.
- Install any missing dependencies you need (e.g., `scikit-learn`, `pandas`).
- Create the `/home/user/artifacts/` directory if it does not exist.