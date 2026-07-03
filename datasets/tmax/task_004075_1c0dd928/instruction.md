You are a Data Engineer building an ETL and analysis pipeline for server telemetry data. 

You have been given a raw dataset of server metrics located at `/home/user/data/raw/metrics.csv`. 
Your task is to write and execute a Python script (`/home/user/pipeline.py`) that performs Extraction, Transformation, and Loading (ETL) along with statistical analysis.

The pipeline must perform the following steps exactly:

1. **Schema Enforcement & Data Cleaning:**
   - Read the CSV file `/home/user/data/raw/metrics.csv`. The columns are `cpu_usage`, `ram_usage`, `disk_io`, and `net_tx`.
   - Filter out any invalid rows to enforce the schema. Valid data must meet these conditions:
     - `0.0 <= cpu_usage <= 100.0`
     - `0.0 <= ram_usage <= 100.0`
     - `disk_io >= 0.0`
     - `net_tx >= 0.0`
   - Drop any rows containing missing (NaN) values.

2. **Correlation & Bootstrap Analysis:**
   - Focus on the cleaned dataset.
   - We want to estimate the stability of the Pearson correlation between `cpu_usage` and `ram_usage`.
   - Perform a bootstrap analysis with exactly **1000** resamples of the cleaned dataset (each resample must be the same size as the cleaned dataset, sampled with replacement).
   - Use `numpy.random.seed(42)` immediately before starting your bootstrap loop to ensure reproducibility.
   - Calculate the Pearson correlation coefficient between `cpu_usage` and `ram_usage` for each resample.
   - Compute the mean, 2.5th percentile (lower bound), and 97.5th percentile (upper bound) of these 1000 correlation values. Use `numpy.percentile`.

3. **Modeling & Hyperparameter Tuning:**
   - Train a Ridge Regression model (`sklearn.linear_model.Ridge`) to predict `net_tx` using `cpu_usage`, `ram_usage`, and `disk_io` as features.
   - Use `sklearn.model_selection.GridSearchCV` to perform 5-fold cross-validation.
   - Test the following `alpha` values: `[0.1, 1.0, 10.0, 100.0]`.
   - Use the default scoring metric (R-squared).
   - Set `random_state=42` if/where the cross-validation or model requires it (Note: standard Ridge and KFold in this configuration might not need it, but use `KFold(n_splits=5, shuffle=True, random_state=42)` for the CV splitter to ensure deterministic folds).

4. **Output Generation:**
   - Save the results of your analysis to `/home/user/output/report.json`.
   - The JSON file must have exactly this structure and naming:
     ```json
     {
       "valid_row_count": <int>,
       "cpu_ram_corr_mean": <float>,
       "cpu_ram_corr_lower": <float>,
       "cpu_ram_corr_upper": <float>,
       "best_alpha": <float>,
       "best_cv_score": <float>
     }
     ```
   - All floats should be rounded to 4 decimal places.

Run your script to produce the final `report.json` file. Ensure the directories exist before writing to them.