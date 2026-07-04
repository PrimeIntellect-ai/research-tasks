You are a data analyst at a manufacturing company. We collect massive amounts of machine telemetry and text-based diagnostic logs. You need to process a large dataset of these logs to prepare it for a machine learning model.

Your task has three parts:

1. **Data Cleaning:**
   Read the dataset located at `/home/user/data/telemetry.csv`. 
   This file contains three columns: `id`, `sensor_val`, and `log_message`.
   The `sensor_val` column contains missing values (NaNs) and extreme outliers. 
   You must clean this column by:
   - Imputing missing values with the global median of the valid `sensor_val` entries.
   - Capping (clipping) the outliers to the 1st and 99th percentiles of the (post-imputation) dataset.

2. **Feature Engineering (Reverse-Engineering an Oracle):**
   We have a proprietary feature extraction algorithm that combines the cleaned sensor value and the log message into a single `feature_score`. We cannot give you the source code, but we have provided a compiled, stripped Linux binary at `/app/feature_oracle`.
   Usage: `/app/feature_oracle <cleaned_sensor_val> "<log_message>"`
   Example: `/app/feature_oracle 12.5 "Valve pressure stabilized"`
   
   The dataset has 500,000 rows. Running this binary via subprocess for every row will take hours and is unacceptable. You must deduce the underlying mathematical and tokenization logic of the oracle by testing it with different inputs in your terminal. Once you understand the formula, implement a vectorized equivalent in Python to process the entire dataset quickly.

3. **Large-scale Storage:**
   Save the final processed dataset as a Parquet file at `/home/user/processed_features.parquet`.
   The file must contain exactly three columns: `id`, `cleaned_sensor_val`, and `feature_score`.

**Constraints & Verification:**
- Use Python (pandas, numpy, pyarrow/fastparquet) for your final script.
- The automated grading system will compare your `feature_score` values against the true expected mathematical values. The Mean Absolute Error (MAE) must be strictly less than 0.01.