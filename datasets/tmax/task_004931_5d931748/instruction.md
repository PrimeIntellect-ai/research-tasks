You are acting as a data analyst. A junior team member has written a script `/home/user/bayesian_model.py` to perform Bayesian Linear Regression on a dataset `/home/user/data.csv`. 

The dataset contains 100 rows with two features, `X1` and `X2`, and a continuous target `y`.

However, the junior analyst made a critical mistake: they applied `StandardScaler` to the *entire* dataset before splitting it into training and testing sets, resulting in data leakage.

Your task is to fix the script and extract some specific metrics:
1. Modify `/home/user/bayesian_model.py` to properly prevent data leakage. The data must be split *first* (the first 80 rows for training, the last 20 rows for testing). The `StandardScaler` must be fitted **only** on the training features, and then used to transform both the training and testing features.
2. Calculate the empirical covariance matrix of the scaled *training* features `X1` and `X2`. Use the default unbiased estimator (e.g., `ddof=1` if using pandas or numpy).
3. Compute the test set predictions (predictive mean) using the updated, leakage-free Bayesian Linear Regression model.
4. Save the results to a file named `/home/user/results.json` with the following exact structure:

```json
{
  "train_feature_covariance": [[cov_x1_x1, cov_x1_x2], [cov_x2_x1, cov_x2_x2]],
  "test_predictions": [pred_1, pred_2, ..., pred_20]
}
```

Ensure numerical accuracy. The test predictions should be rounded to 4 decimal places, and the covariance values should be rounded to 4 decimal places.