You are an AI assistant helping a data researcher fix a machine learning script. The researcher is organizing their experimental datasets and scripts in `/home/user/research/`. 

They have a script, `/home/user/research/train_model.py`, that trains a model on `/home/user/research/data.csv`. However, the researcher has noticed their cross-validation scores are overly optimistic. They suspect a "data leakage" issue where information from the validation folds leaks into the training phase because missing value imputation and scaling are currently applied to the *entire* dataset using `fit_transform` before splitting.

Your task is to rewrite `train_model.py` to fix this data leak and perform proper hyperparameter tuning.

Requirements for the new `train_model.py`:
1. Load `/home/user/research/data.csv`. The target variable is `target`. All other columns are features.
2. Build a strict `scikit-learn` `Pipeline` to prevent data leakage. The pipeline must contain:
   - Step 1 (named 'imputer'): A `SimpleImputer`.
   - Step 2 (named 'scaler'): A `StandardScaler`.
   - Step 3 (named 'model'): A `Ridge` regressor (use `random_state=42`).
3. Use `GridSearchCV` to tune the pipeline. The cross-validation must use `KFold` with `n_splits=5`, `shuffle=True`, and `random_state=42`.
4. The parameter grid must explore:
   - `imputer__strategy`: `['mean', 'median']`
   - `model__alpha`: `[0.1, 1.0, 10.0, 100.0]`
5. Fit the `GridSearchCV` on the features and target.
6. Extract the best hyperparameters and the best mean cross-validated score (`best_score_`).
7. Save the results as a JSON file at `/home/user/research/results.json` with the following exact keys:
   - `"best_alpha"` (float)
   - `"best_imputer_strategy"` (string)
   - `"best_cv_score"` (float, rounded to exactly 4 decimal places)

You should install any necessary dependencies, modify the script, execute it, and verify the `results.json` file is created correctly.