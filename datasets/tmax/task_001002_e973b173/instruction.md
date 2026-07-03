You are an MLOps engineer tasked with tracking, analyzing, and auditing a set of model experiment artifacts. The system has generated multiple prediction logs across different environments, and we suspect some artifacts are corrupted due to anomalous variance in their predictions.

You must perform a multi-phase analysis combining data joining, bootstrapping, feature engineering, and classification, all while strictly configuring your numerical library threads.

**Data Location:**
You have a data directory at `/home/user/mlops_data/` containing:
1. `metadata.db`: A SQLite database with a table `experiments` (columns: `artifact_id`, `model_type`, `training_time`, `is_anomalous`).
2. `logs/`: A directory containing multiple CSV files named `run_<artifact_id>.csv`. Each CSV has two columns: `y_true` and `y_pred`.

**Phase 1: Environment Configuration**
Write a Python script at `/home/user/audit.py`. To ensure deterministic and constrained execution in our CI pipeline, your script must strictly execute with a single thread for numerical operations. Before importing any numerical libraries (like numpy, pandas, or scikit-learn) in your script, you must set the following environment variables to `"1"`:
`OMP_NUM_THREADS`, `OPENBLAS_NUM_THREADS`, `MKL_NUM_THREADS`, `VECLIB_MAXIMUM_THREADS`, `NUMEXPR_NUM_THREADS`.

**Phase 2: Joining and Bootstrapping (Feature Engineering)**
For each `artifact_id` found in the `logs/` directory:
1. Load the corresponding predictions and calculate the Root Mean Squared Error (RMSE).
2. Compute the 95% Confidence Interval (2.5th and 97.5th percentiles) of the RMSE using a bootstrap method. 
   - **Bootstrap Specification:** Perform exactly 200 bootstrap iterations. For iteration `i` (from 0 to 199), sample the DataFrame using `sklearn.utils.resample(df, replace=True, random_state=i)`.
   - Calculate the RMSE for each sample.
   - Calculate the 2.5th and 97.5th percentiles of these 200 RMSE values using `numpy.percentile` (default interpolation).

**Phase 3: Multi-source Joining & Classification**
1. Read the `experiments` table from `metadata.db`.
2. Join your engineered bootstrap features (`rmse_mean` [the average of the 200 bootstrap RMSEs], `rmse_lower`, `rmse_upper`) with the metadata. Also include the original `training_time` as a feature.
3. You will find that some rows have `is_anomalous` as `1` or `0`, while others are missing (NaN/NULL).
4. Train a Logistic Regression model (`sklearn.linear_model.LogisticRegression` with `random_state=42`, default parameters) on the rows where `is_anomalous` is known. The features to use are: `training_time`, `rmse_mean`, `rmse_lower`, `rmse_upper`.
5. Predict the `is_anomalous` status for the rows where it is missing.

**Output Generation:**
Your script must output a final CSV file at `/home/user/audit_results.csv` containing the following columns exactly:
`artifact_id`, `rmse_lower`, `rmse_upper`, `predicted_anomalous`
- `artifact_id`: String
- `rmse_lower` and `rmse_upper`: Float, rounded to 4 decimal places.
- `predicted_anomalous`: Integer (0 or 1). If the row was in the training set (already had a label), output its original label. If it was missing, output the predicted label.

Sort the CSV by `artifact_id` in ascending order.