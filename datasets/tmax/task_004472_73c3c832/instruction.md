You are a data engineer building a reproducible ETL and modeling pipeline for sensor calibration. 

We have a raw dataset located at `/home/user/sensor_data.csv` containing four columns: `temp`, `pressure`, `humidity`, and the target variable `error_margin`. 

Your task is to create and run a Python script at `/home/user/etl_pipeline.py` that performs the following steps:
1. **Data Schema Enforcement**: Read the CSV file. Filter out any rows that violate these physical constraints:
   - `temp` must be between -50.0 and 50.0 (inclusive).
   - `humidity` must be between 0.0 and 100.0 (inclusive).
   - `pressure` must be strictly positive (> 0).
   Drop any rows containing missing values (NaNs).
2. **Analysis Environment Setup**: Ensure exact reproducibility by setting the `numpy` random seed to `42`. 
3. **Cross-validation & Hyperparameter Tuning**: 
   - Separate the features (`temp`, `pressure`, `humidity`) and the target (`error_margin`).
   - Use `sklearn.linear_model.RidgeCV` to find the best regularization parameter (`alpha`). 
   - Test the following alphas: `[0.01, 0.1, 1.0, 10.0, 100.0]`.
   - Use 5-fold cross-validation (`cv=5`).
   - Fit the `RidgeCV` model on the filtered dataset.
4. **Metric Logging**: Calculate the standard R² score of the fitted model on the exact same filtered dataset used for training. 
5. Write the best alpha and the rounded R² score (rounded to exactly 4 decimal places) to a JSON file at `/home/user/model_metrics.json`.

The JSON file must have exactly this structure:
```json
{
  "best_alpha": 1.0,
  "r2_score": 0.1234
}
```

Write the script, run it, and ensure the `/home/user/model_metrics.json` file is successfully created.