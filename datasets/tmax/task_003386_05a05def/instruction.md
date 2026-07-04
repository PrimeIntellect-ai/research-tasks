You are an MLOps engineer tasked with building a reproducible experiment pipeline. We have a raw dataset located at `/home/user/raw_data.csv`. Your objective is to create a Python script that processes this data, engineers new features, trains specific classification models, and tracks the experiment artifacts and metrics using a lightweight JSON Lines format.

Please accomplish the following:
1. **Environment Setup**: Ensure your Python environment has `numpy`, `pandas`, and `scikit-learn` installed.
2. **Feature Engineering**: 
   - Load `/home/user/raw_data.csv`. The dataset contains features `f0`, `f1`, `f2`, `f3`, `f4` and a target column `target`.
   - Create a new feature `f5` which is the product of `f0` and `f1` (i.e., `f5 = f0 * f1`).
   - Standardize all features (`f0` through `f5`) using `sklearn.preprocessing.StandardScaler`.
3. **Modeling & Experiment Tracking**:
   - Evaluate two models using 5-fold cross-validation (`sklearn.model_selection.KFold` with `n_splits=5`, `shuffle=True`, `random_state=42`):
     a. `LogisticRegression` with `C=1.0` and `random_state=42`.
     b. `RandomForestClassifier` with `n_estimators=50`, `max_depth=5`, and `random_state=42`.
   - Compute the mean accuracy across the 5 folds for each model.
   - Log the results to an experiment tracking file at `/home/user/metrics.jsonl`. Each line must be a valid JSON object representing one model's experiment. The JSON must exactly match this schema:
     `{"model_name": "<LogisticRegression or RandomForestClassifier>", "mean_cv_accuracy": <float>, "hyperparameters": <dict of the specified hyperparams>}`
4. **Artifact Storage**:
   - Identify the model that achieved the highest `mean_cv_accuracy`.
   - Train this best model on the *entire* engineered dataset (no train/test split for the final fit).
   - Save the fitted model pipeline (or just the model, if scaled features are passed) to `/home/user/best_model.pkl` using `joblib` or `pickle`.

Ensure all file paths are strictly adhered to. Your final deliverables are the `metrics.jsonl` log file and the `best_model.pkl` file.