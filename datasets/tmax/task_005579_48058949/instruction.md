You are an MLOps engineer tasked with fixing a data processing pipeline and tracking experiment metrics. 

You have a dataset located at `/home/user/data.csv`. Some columns that represent counts or integer values (`age` and `clicks`) were silently cast to floats because of missing values (NaNs).

Your task is to write and run a script (in the language of your choice, though Python with pandas/scikit-learn is recommended) that performs the following steps:
1. Load `/home/user/data.csv`.
2. Identify the `age` and `clicks` columns. Impute any missing values (NaNs) in these columns with their respective medians, and then cast both columns explicitly to integer types.
3. The features for your model are `age`, `clicks`, and `duration`. The target variable is `revenue`.
4. Perform hyperparameter tuning for a Ridge Regression model. Use 5-fold cross-validation (`KFold`, with `shuffle=True` and `random_state=42`) to evaluate `alpha` values of `[0.1, 1.0, 10.0]`. Determine the `best_alpha` that maximizes the mean R-squared score across the 5 folds.
5. Record the mean R-squared score of the best alpha on the original dataset (`mean_cv_r2_original`).
6. To estimate the stability of this CV score, perform 100 bootstrap iterations. 
   - Set the random seed to `42` right before the bootstrap loop (`np.random.seed(42)` or equivalent).
   - In each iteration, create a bootstrap sample of the imputed dataset (sample with replacement, same size as the original data).
   - On this bootstrap sample, compute the 5-fold CV mean R-squared score using Ridge Regression with the `best_alpha` (again using `KFold(n_splits=5, shuffle=True, random_state=42)`).
   - Calculate the standard deviation of these 100 mean CV scores (`bootstrap_se_r2`).
7. Save the experiment artifacts to `/home/user/experiment.json` in the exact following format:
```json
{
  "best_alpha": 1.0,
  "mean_cv_r2_original": 0.8523,
  "bootstrap_se_r2": 0.0154
}
```
(Round floating point values to 4 decimal places in the JSON).