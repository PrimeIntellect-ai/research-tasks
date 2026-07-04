You are an MLOps engineer reviewing a colleague's experiment artifact pipeline. 

There is a Python script located at `/home/user/evaluate.py` that prepares a synthetic dataset, scales the features, trains a Logistic Regression model, and measures both the test accuracy and inference time. 

However, your colleague made a classic mistake: there is **data leakage** in the pipeline. Specifically, the feature scaling (`fit_transform`) is applied to the entire dataset *before* the `train_test_split`. This means information from the test set leaks into the training process, leading to overly optimistic accuracy metrics.

Your task is to:
1. Identify and fix the data leakage bug in `/home/user/evaluate.py`. Refactor the code so that the dataset is split *first*, and the scaler is `fit` ONLY on the training data, then used to `transform` both the training and test data.
2. Maintain all existing random seeds (`42` for data generation, splitting, and model initialization) to ensure reproducibility.
3. Keep the inference benchmarking logic intact (measuring the time it takes to predict on the test set).
4. Run the fixed script. It should write the corrected metrics to `/home/user/metrics.json`.

The output file `/home/user/metrics.json` must exactly match this format:
```json
{
  "accuracy": 0.95,
  "inference_time": 0.00123
}
```
(Note: the accuracy value will change once you fix the leakage. Leave the inference time as dynamically calculated by the script).