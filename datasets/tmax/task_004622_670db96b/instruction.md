As an MLOps engineer, you are auditing a batch of recent machine learning experiments. You suspect that one of the experiments has a data leakage issue that artificially inflated its evaluation accuracy. 

In the directory `/home/user/experiments/scripts/`, there are 100 Python training scripts (named `exp_001.py` through `exp_100.py`). Most scripts correctly scale their test data using `scaler.transform(X_test)`. However, exactly one script mistakenly uses `fit_transform` on the test data (`X_test`), causing a data leak between the train and test sets.

Your task is to:
1. Identify the Python script that contains this data leak.
2. Look up the corresponding model artifact path for this specific experiment in the log file located at `/home/user/experiments/logs/metrics.csv`. The CSV contains the columns `experiment_name,accuracy,model_artifact`.
3. Write ONLY the absolute path of the model artifact for the leaked experiment into a new file at `/home/user/leaked_model.txt`.

The file `/home/user/leaked_model.txt` should contain a single line with the exact path to the `.joblib` model artifact.