You are an AI assistant helping a data scientist debug and improve a machine learning pipeline. 

In `/home/user/`, you will find two files:
1. `data.csv`: A binary classification dataset containing missing values and outliers.
2. `leaky_train.py`: A script that trains a Random Forest model using 5-fold cross-validation.

The current script (`leaky_train.py`) has a critical data leakage flaw: it applies `SimpleImputer` and `StandardScaler` to the *entire* feature set before performing cross-validation. This leads to overly optimistic cross-validation scores because information from the validation folds leaks into the training step of each fold.

Your task is to fix this leakage, improve the robustness to outliers, tune hyperparameters, and quantify the leakage effect.

Specifically, write a new Python script `/home/user/fixed_train.py` that does the following:
1. **Pipeline Construction**: Create an `sklearn.pipeline.Pipeline` that chains imputation (`SimpleImputer(strategy='mean')`), scaling, and the classifier (`RandomForestClassifier(random_state=42)`).
2. **Outlier Handling**: Replace `StandardScaler` with `RobustScaler` within the pipeline to better handle outliers present in the dataset.
3. **Hyperparameter Tuning**: Use `GridSearchCV` with 5-fold cross-validation (`cv=5`) to tune the random forest. Use the following parameter grid:
   - `classifier__n_estimators`: `[50, 100]`
   - `classifier__max_depth`: `[5, 10, None]`
   (Make sure the step name in the pipeline matches the prefix, e.g., `'classifier'`).
4. **Save Metrics**: Fit the `GridSearchCV` on the full feature set `X` and target `y` from `data.csv`. Save the `best_params_` and the best `mean_test_score` (rounded to 4 decimal places) into a JSON file at `/home/user/best_model.json`.
   Example format: `{"best_params": {"classifier__max_depth": 5, "classifier__n_estimators": 50}, "cv_score": 0.8521}`
5. **Hypothesis Testing**: To quantify the leakage from the original script, calculate the 5-fold cross-validation accuracy scores using `cross_val_score` for:
   - The original *leaky* approach (impute and scale the entire `X` first, then evaluate `RandomForestClassifier(n_estimators=100, random_state=42)`).
   - The *fixed* approach using a standard pipeline (Impute -> RobustScaler -> `RandomForestClassifier(n_estimators=100, random_state=42)`).
   Both must use 5-fold CV without shuffling (default `cross_val_score` behavior). Perform a paired t-test (using `scipy.stats.ttest_rel`) comparing the 5 fold scores of the leaky model vs. the fixed model. Save the resulting p-value, rounded to 4 decimal places, to `/home/user/p_value.txt`.

Ensure your script runs successfully and produces the required output files. You must use `random_state=42` for any model that requires it to ensure reproducible results. Do not modify `data.csv`.