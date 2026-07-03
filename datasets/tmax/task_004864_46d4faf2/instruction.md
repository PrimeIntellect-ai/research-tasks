You are an AI assistant helping a data researcher organize their datasets and run a baseline experiment.

The researcher has a dataset located at `/home/user/data.csv` with the following columns: `ID`, `Feature_A`, `Feature_B`, and `Target`. 

Write and execute a Python script at `/home/user/pipeline.py` that performs the following steps:

1. **Feature Engineering**: Load the CSV and create a new column named `Ratio` which is `Feature_A` divided by `Feature_B`.
2. **Data Cleaning & Schema Enforcement**: Division by zero will introduce infinite values. Replace any `inf` or `-inf` in the dataset with `NaN`. Then, drop all rows containing any `NaN` values. 
3. **Data Schema**: Ensure the `ID` column is strictly of type `int64` (the introduction of `NaN`s in intermediate steps often silently converts integer columns to floats in pandas, which breaks downstream systems). Ensure `Feature_A`, `Feature_B`, `Ratio`, and `Target` are `float64`. Save this cleaned dataframe to `/home/user/clean_data.parquet`.
4. **Cross-Validation & Hyperparameter Tuning**: Using `sklearn`, set up a `Ridge` regression predicting `Target` from features `['Feature_A', 'Feature_B', 'Ratio']`. Use `GridSearchCV` with 5-fold cross-validation (`cv=5`) to test `alpha` values `[0.1, 1.0, 10.0]`. Use `scoring='neg_mean_squared_error'`.
5. **Experiment Tracking**: Extract the best `alpha` and its corresponding mean validation MSE (convert the negative MSE to a positive value). Save these to a JSON file at `/home/user/experiment.json` with the exact keys:
   `{"best_alpha": <float>, "best_cv_mse": <float>}`. Round the `best_cv_mse` to exactly 4 decimal places.

Run your script to produce both `/home/user/clean_data.parquet` and `/home/user/experiment.json`.