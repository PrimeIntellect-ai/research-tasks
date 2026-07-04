You are an MLOps engineer reviewing a colleague's anomaly detection pipeline. The pipeline processes network telemetry data, performs dimensionality reduction, and trains a logistic regression model. However, the current code has a critical data leakage issue, and it lacks statistical evaluation of the generated embeddings.

Your tasks are:

1. **Fix Data Leakage**: Edit the Python script at `/home/user/pipeline.py`. Currently, it applies `StandardScaler` and `PCA(n_components=2)` to the entire dataset *before* splitting into train and test sets. Modify the script so that the train-test split (`test_size=0.2, random_state=42`) occurs *first*. Then, fit the scaler and PCA **only** on the training data, and use them to transform both the training and test sets. Retain the `LogisticRegression(random_state=42)` model.

2. **Add Hypothesis Testing**: After transforming the test set, extract the values of the first principal component (`PC1`, which is the first column of the transformed data) for the test set. Use `scipy.stats.ttest_ind` (two-sided) to perform an independent t-test comparing the `PC1` values of instances where the true label is `0` versus those where the true label is `1` in the test set.

3. **Output Metrics**: Ensure the script saves the results to `/home/user/results.json`. The JSON file must contain exactly these two keys:
   - `"accuracy"`: The test set accuracy of the Logistic Regression model (float).
   - `"p_value"`: The p-value from the t-test (float).

4. **Environment Setup Script**: Create a bash script at `/home/user/run.sh` that:
   - Creates a Python virtual environment at `/home/user/venv`.
   - Activates it.
   - Installs `pandas`, `scikit-learn`, and `scipy`.
   - Runs `/home/user/pipeline.py`.
   Make sure `/home/user/run.sh` is executable (`chmod +x`).

The input dataset is located at `/home/user/telemetry.csv`. Do not modify this file.