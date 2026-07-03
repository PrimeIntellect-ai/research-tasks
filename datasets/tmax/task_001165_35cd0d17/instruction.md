You are a data engineer responsible for building robust, reproducible ETL pipelines. Your current assignment is to process an incoming dataset, enforce its schema, and test a predictive modeling pipeline for stability across different random seeds.

You have been provided with the following files in `/home/user/`:
1. `raw_data.csv`: A dataset containing features `f1`, `f2`, `cat`, and a target variable `target`.
2. `schema.json`: A JSON file defining the valid data types and bounds for the features.
3. `pipeline_spec.json`: A JSON file specifying the modeling pipeline architecture and hyperparameter grid.

**Step 1: Data Schema Enforcement**
Write a Python script to load `raw_data.csv` and filter out any rows that do not strictly comply with `schema.json`. 
The schema enforcement rules:
- `f1`: Must be a valid float.
- `f2`: Must be a valid float AND strictly greater than the `min_value` defined in the schema.
- `cat`: Must be a valid integer AND its value must exist in the `allowed_values` list defined in the schema.
- `target`: Must be a valid float.
- Drop any row containing missing/null values, or values that cannot be parsed to the required type, or values out of bounds.

**Step 2: Model Architecture Reconstruction & Tuning**
Using `scikit-learn`, construct a Pipeline based exactly on `pipeline_spec.json`. The spec defines a two-step pipeline: a scaler and a regressor.
Perform hyperparameter tuning on the filtered (clean) dataset using `GridSearchCV`. You must tune the regressor's `alpha` parameter using the grid provided in the spec.

**Step 3: Pipeline Reproducibility Testing**
To ensure the pipeline tuning is stable, run the `GridSearchCV` using a `KFold` cross-validator with `n_splits=3` and `shuffle=True`. You must test the pipeline across three specific random states for the KFold splitting: `[10, 20, 30]`. 
(Use the default scoring metric for the regressor, which is R^2).

**Step 4: Output Generation**
Generate a report of your findings and save it to `/home/user/etl_output.json`. The JSON file must perfectly match this structure:

```json
{
  "valid_rows_count": <integer, number of rows after schema enforcement>,
  "reproducibility_test": [
    {
      "seed": 10,
      "best_alpha": <float, best alpha found>,
      "best_cv_score": <float, mean_test_score of the best estimator, rounded to 4 decimal places>
    },
    {
      "seed": 20,
      "best_alpha": <float>,
      "best_cv_score": <float, rounded to 4 decimal places>
    },
    {
      "seed": 30,
      "best_alpha": <float>,
      "best_cv_score": <float, rounded to 4 decimal places>
    }
  ]
}
```