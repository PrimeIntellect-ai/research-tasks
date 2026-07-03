You are an MLOps engineer tasked with standardizing experiment tracking artifacts for a new Bayesian modeling pipeline. 

I have placed a dataset at `/home/user/data.csv` and a JSON schema for our experiment tracking system at `/home/user/schema.json`. 

Please perform the following steps:
1. Set up your Python environment by installing any necessary libraries (e.g., `scikit-learn`, `pandas`, `jsonschema`).
2. Write a Python script at `/home/user/experiment.py` that does the following:
   - Loads the dataset `/home/user/data.csv`. The target variable is in the `target` column, and the rest are features.
   - Initializes a `BayesianRidge` regressor from `scikit-learn`.
   - Performs hyperparameter tuning using `GridSearchCV` with 3-fold cross-validation. Tune the parameters `alpha_1` and `lambda_1` over the exact grid: `[1e-6, 1e-5, 1e-4]`. Leave all other parameters at their defaults.
   - Extracts the best hyperparameters and the best mean cross-validation score (R-squared).
   - Formats the results into a Python dictionary containing the keys: `"model"` (must be exactly `"BayesianRidge"`), `"best_alpha_1"`, `"best_lambda_1"`, and `"cv_score"`.
   - Enforces the data schema by validating this dictionary against `/home/user/schema.json` using the `jsonschema` library.
   - If validation passes, saves the dictionary as a JSON file at `/home/user/artifact.json`.
3. Execute your script to generate `/home/user/artifact.json`.

Ensure that the output file exactly matches the schema and is strictly valid JSON.