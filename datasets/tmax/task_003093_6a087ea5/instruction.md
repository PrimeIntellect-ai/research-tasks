You are an AI assistant helping a materials researcher organize a newly collected dataset of material properties. 

The researcher has an initial dataset located at `/home/user/data/unorganized_data.csv`. This file contains experimental measurements with the following columns: `mass`, `volume`, and `class`. 

Unfortunately, the data collection sensors occasionally produce faulty readings, and the dataset is messy. Your task is to write and execute a Python script that cleans the dataset (enforcing a strict data schema) and then trains a tuned Bayesian classification model on it.

Please perform the following steps:

1. **Schema Enforcement & Data Cleaning**:
   Read `/home/user/data/unorganized_data.csv` and filter it to create a clean dataset. 
   A valid row MUST meet ALL of the following criteria:
   - `mass` is a valid number strictly greater than 0.
   - `volume` is a valid number strictly greater than 0.
   - `class` is an integer exactly equal to either 0 or 1.
   - The row contains no missing/null values.
   
   Save the filtered dataset to `/home/user/data/organized_data.csv` (include the header, keep the same column order, and preserve the original index).

2. **Bayesian Classification & Hyperparameter Tuning**:
   Using the cleaned dataset, predict `class` using `mass` and `volume` as features.
   - Use `GaussianNB` from `sklearn.naive_bayes`.
   - Perform hyperparameter tuning using `GridSearchCV` to find the best `var_smoothing` value. 
   - Use exactly these values for `var_smoothing`: `[1e-9, 1e-7, 1e-5, 1e-3, 1e-1]`.
   - Use default 5-fold cross-validation (`cv=5`, without shuffling).

3. **Reporting**:
   Generate a JSON report at `/home/user/data/model_results.json` containing the following exact keys:
   - `"best_var_smoothing"`: The best `var_smoothing` parameter found (float).
   - `"best_cv_score"`: The best mean cross-validation accuracy score (float, rounded to exactly 4 decimal places).
   - `"cleaned_row_count"`: The number of rows in your cleaned dataset (integer).

Note: You can use `pandas`, `scikit-learn`, and standard built-in Python libraries. Ensure your script creates all requested output files in the correct format.