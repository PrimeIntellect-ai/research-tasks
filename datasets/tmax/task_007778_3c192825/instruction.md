You are a data analyst working on a new classification model. I need you to find the best hyperparameter configuration for a Random Forest model and benchmark its inference latency. 

You have been provided with a dataset at `/home/user/data.csv`.

Please write and execute a Python script that performs the following steps:
1. Ensure the required packages (`pandas`, `scikit-learn`) are installed.
2. Load `/home/user/data.csv`. The target column is named `target`. All other columns are features.
3. Split the data into a training set (80%) and a test set (20%) using `train_test_split` with `random_state=42`.
4. Perform a grid search using 5-fold cross-validation (`GridSearchCV`) on the training set to tune a `RandomForestClassifier` (initialize it with `random_state=42`). 
5. Search the following parameter grid:
   - `n_estimators`: [10, 50, 100]
   - `max_depth`: [None, 5, 10]
6. Identify the best model based on cross-validated accuracy.
7. Benchmark the inference performance of the *best* model on the test set. Specifically, measure the total time it takes to run `predict()` on the *entire* test set. Run this prediction step 100 times in a loop and calculate the average time per run in milliseconds.
8. Save your findings to a JSON file at `/home/user/report.json` with the following exact keys:
   - `"best_n_estimators"`: (integer)
   - `"best_max_depth"`: (integer or null)
   - `"cv_accuracy"`: (float, the best mean cross-validated accuracy rounded to 4 decimal places)
   - `"avg_inference_time_ms"`: (float, the average inference time per test set prediction over the 100 runs, in milliseconds, rounded to 2 decimal places)

Make sure the final JSON file is properly formatted.