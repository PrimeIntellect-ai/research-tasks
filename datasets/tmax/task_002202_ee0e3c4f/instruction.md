You are an MLOps engineer debugging an experiment tracking pipeline. 

In `/home/user/mlops_experiment`, there is a script named `train.py` and a dataset `data.csv`. The script currently has a critical data leakage bug: it applies `StandardScaler().fit_transform()` and fills missing values on the *entire* dataset before performing the train-test split. This leads to overly optimistic evaluation metrics.

Your task is to fix this script and track the experiment properly:
1. Modify `train.py` to eliminate the data leak. You must use a `scikit-learn` `Pipeline` to chain a `SimpleImputer(strategy='mean')`, a `StandardScaler()`, and the `RandomForestClassifier(random_state=42)`.
2. Ensure `train_test_split` (with `test_size=0.2, random_state=42`) is called *before* any transformations are applied.
3. Fit the pipeline on the training data and evaluate it on the test data.
4. Save the trained pipeline to `/home/user/mlops_experiment/model.pkl` using `joblib`.
5. The script must output a JSON file at `/home/user/mlops_experiment/run_metadata.json` containing the experiment tracking data. The JSON must exactly match this structure:
```json
{
  "test_accuracy": <float>,
  "model_path": "/home/user/mlops_experiment/model.pkl"
}
```

Do not modify the dataset itself. Run your fixed script to generate the model and the metadata file.