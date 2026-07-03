You are a data scientist taking over a project to clean a messy dataset and build a predictive model. 

We have a machine learning pipeline that needs to predict the `income` of individuals based on their demographic information and employment details. However, the data contains highly messy categorical columns (`job_title` and `city`) with typos and inconsistencies. 

To handle this, we rely on the `category_encoders` Python package. For security and versioning reasons, our platform engineering team has vendored the source code of `category_encoders` at `/app/category_encoders`. 

However, there is an issue: the vendored package is currently broken. A recent internal commit introduced a bug, preventing the `TargetEncoder` from functioning correctly. 

Your tasks are:
1. **Fix the Vendored Package**: Inspect the source code of `category_encoders` in `/app/category_encoders`. Find and fix the syntax or import bug that breaks the `TargetEncoder`. After fixing it, install the package in editable mode (`pip install -e /app/category_encoders`).
2. **Data Cleaning and Modeling Pipeline**: 
   - Write a reproducible Python script `/home/user/run_pipeline.py`.
   - The script must read the training data from `/home/user/data/train.csv`. 
   - Use `category_encoders.TargetEncoder` to encode the `job_title` and `city` columns.
   - Train a regression model (e.g., `HistGradientBoostingRegressor` or `RandomForestRegressor` from `scikit-learn`) to predict the continuous `income` column.
   - You must use experiment tracking by saving your chosen hyperparameters and cross-validation scores to a JSON file at `/home/user/experiment.json`.
3. **Prediction**:
   - The script must then load `/home/user/data/test.csv` (which has all columns except `income`).
   - Generate predictions for the test set.
   - Save the predictions to `/home/user/predictions.csv`. The file should contain exactly one column named `predicted_income` with the floating-point prediction for each row in the test set, in the exact same order as `test.csv`.

**Constraints & Verification**:
Your model must generalize well. The final predictions in `/home/user/predictions.csv` will be evaluated against a hidden set of true values using the R-squared ($R^2$) metric. You must achieve an $R^2$ score of at least `0.65` on the test set. Ensure your pipeline appropriately handles missing values if there are any.