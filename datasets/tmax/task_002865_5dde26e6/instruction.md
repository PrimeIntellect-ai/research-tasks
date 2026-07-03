You are tasked with fixing a machine learning pipeline and adding benchmarking metrics.

In `/home/user`, there is a Python script named `train_model.py`. This script joins two data sources (`users.csv` and `transactions.csv`), trains a Logistic Regression classifier to predict user churn, and prints the accuracy.

However, the pipeline has a critical flaw: **data leakage**. The features are scaled using `StandardScaler.fit_transform()` on the entire dataset *before* it is split into training and test sets. 

Your objectives are:
1. **Fix the Data Leakage**: Modify `train_model.py` so that the `StandardScaler` is properly fitted *only* on the training data, and then used to transform both the training and test data.
2. **Ensure Reproducibility**: When splitting the dataset, use a `test_size` of `0.2` and set `random_state=42`. Ensure the Logistic Regression model is initialized with `random_state=42`.
3. **Inference Benchmarking**: Wrap the `model.predict()` call on the test set with timing code to measure the inference time. 
4. **Save Metrics**: Save the accuracy and the inference time to `/home/user/metrics.json` in the following format:
   ```json
   {
       "accuracy": 0.85,
       "inference_time_seconds": 0.0012
   }
   ```
5. **Save Predictions**: Save the predictions for the test set to `/home/user/predictions.csv`. The file must contain exactly two columns: `user_id` and `predicted_churn`, including the header.

Modify the code as needed, run it, and verify that the output files are correctly generated.