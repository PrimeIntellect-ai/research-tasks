You are an MLOps engineer tasked with fixing a machine learning pipeline and tracking its experiment artifacts. 

We have a partially completed script at `/home/user/scripts/pipeline.py`. The script reads two CSV files, merges them, and prepares the data for model training. However, there is a data preprocessing bug: when the dataframes are merged using a left join, missing values are introduced in the `category_id` column, which silently converts the entire column from integers to floats. 

Your tasks are:
1. **Fix the Data Pipeline:** 
   Modify `/home/user/scripts/pipeline.py` so that any missing values in the `category_id` column after the merge are filled with `-1`, and the column is explicitly cast back to an integer type (`int`) before training.
   
2. **Implement Cross-Validation and Hyperparameter Tuning:**
   Complete the `run_experiment()` function in the script to perform a 5-fold cross-validation using `sklearn.model_selection.GridSearchCV` with a `RandomForestClassifier`.
   Use the following parameter grid:
   - `n_estimators`: `[10, 50]`
   - `max_depth`: `[3, 5]`
   *Note:* Ensure you set `random_state=42` on the `RandomForestClassifier` for reproducibility.

3. **Experiment Tracking:**
   The script must evaluate the grid and save two JSON files to the `/home/user/experiments/` directory:
   - `/home/user/experiments/results.json`: A list of dictionaries tracking the mean cross-validation accuracy for each parameter combination. The format must strictly be:
     `[{"n_estimators": 10, "max_depth": 3, "mean_accuracy": 0.512}, ...]`
     (Float values should be kept as they are returned by sklearn's `cv_results_['mean_test_score']`).
   - `/home/user/experiments/best_params.json`: A single dictionary containing the best hyperparameters found by the grid search. For example:
     `{"n_estimators": 50, "max_depth": 5}`

Run the script to generate the required artifacts. Ensure all paths and output formats match the specifications exactly.