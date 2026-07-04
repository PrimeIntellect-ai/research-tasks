You are an AI assistant helping a machine learning engineer build a reproducible data preparation and training pipeline.

We have a dataset located at `/home/user/dataset.csv` containing mixed data types and missing values. The target variable is named `is_promoted` (binary classification).

Your task is to write a Python script at `/home/user/train_pipeline.py` that performs the following steps:

1. **Load Data:** Read `/home/user/dataset.csv` using pandas. Separate the features (all columns except `is_promoted`) and the target (`is_promoted`).
2. **Build a Reproducible Pipeline:** Create a scikit-learn `Pipeline` that includes:
   - A `ColumnTransformer` for preprocessing:
     - Numeric columns (`age`, `training_score`, `years_of_service`): Impute missing values using the mean, then scale using `StandardScaler`.
     - Categorical columns (`department`, `education`): Impute missing values using the constant value `'missing'`, then apply `OneHotEncoder(handle_unknown='ignore')`.
   - A `RandomForestClassifier` as the final estimator. You MUST set `random_state=42` for the classifier to ensure pipeline reproducibility.
3. **Cross-Validation & Hyperparameter Tuning:** Use `GridSearchCV` to tune the pipeline. Use 3-fold cross-validation (`cv=3`). Search the following parameter grid:
   - Random Forest `n_estimators`: `[10, 50]`
   - Random Forest `max_depth`: `[5, None]`
4. **Experiment Tracking:** Fit the grid search on the entire dataset. Once finished, save the best model (the entire fitted pipeline) to `/home/user/best_pipeline.pkl` using `joblib`.
5. **Log Metrics:** Extract the best cross-validation score (`best_score_`) and the best parameters (`best_params_`) from the grid search. Save these as a JSON file at `/home/user/metrics.json` with exactly the following structure:
   ```json
   {
       "best_cv_score": 0.1234,
       "best_params": {
           "classifier__max_depth": null,
           "classifier__n_estimators": 50
       }
   }
   ```
   *(Note: prefix the parameter names in your grid according to your pipeline step name, e.g., `classifier__n_estimators` if your step is named `classifier`).*

Execute your script to ensure the model and metrics files are generated correctly. Ensure `scikit-learn`, `pandas`, and `joblib` are installed in your environment (you may install them via pip if necessary).