You are a Machine Learning Engineer responsible for preparing data and baseline models for predicting server failures. You have been provided with a dataset of system metrics, but you need to validate statistical assumptions and establish a baseline model.

The raw data will be located at `/home/user/server_metrics.csv` once you begin. It contains the following columns:
`cpu_usage`, `memory_usage`, `disk_io`, `temperature`, and `failure` (target variable, 1=failed, 0=healthy).

Your task has three main requirements:

1. **Hypothesis Testing**: 
   Engineers suspect that `temperature` is significantly higher in servers that fail. Perform an independent two-sample t-test (assuming unequal variances, i.e., Welch's t-test) to compare the `temperature` of healthy servers (`failure=0`) versus failed servers (`failure=1`). 
   - Write the exact p-value (rounded to 4 decimal places) into `/home/user/ttest_pvalue.txt`.

2. **Cross-Validation & Hyperparameter Tuning**:
   Build a baseline `RandomForestClassifier` to predict the `failure` column using the other 4 columns as features.
   Perform a Grid Search with 5-fold cross-validation (standard `KFold` or standard `cross_val_score` without shuffling) to find the best hyperparameters.
   - Use the following parameter grid:
     - `n_estimators`: [50, 100]
     - `max_depth`: [None, 5, 10]
   - **Important for reproducibility**: Set `random_state=42` whenever you instantiate the `RandomForestClassifier`. Do not shuffle the data during cross-validation. 
   - Save the best parameter dictionary as a JSON file at `/home/user/best_params.json`.

3. **Model Validation**:
   Extract the mean cross-validation accuracy of the *best* model found during your grid search.
   - Write this mean accuracy (rounded to 4 decimal places) into `/home/user/best_cv_score.txt`.

You may use any programming language (e.g., Python with `pandas`, `scipy`, `scikit-learn`), but you must execute everything from the terminal and ensure the final output files are correctly formatted and placed in `/home/user`.