You are a data analyst tasked with processing a dataset of sensor readings and building a predictive model while ensuring strict control over numerical library threading.

A dataset is located at `/home/user/sensor_data.csv`. It contains several feature columns (`f1`, `f2`, `f3`, `f4`, `f5`) and a target column (`y`). 

Your objective is to:
1. **Analyze Correlation & Feature Selection:** Compute the Pearson correlation matrix for the feature columns (excluding `y`). Identify any pairs of features that have an absolute correlation strictly greater than 0.85. For each such highly correlated pair, drop the feature that appears later in the CSV column order (e.g., if `f2` and `f4` are highly correlated, drop `f4`).
2. **Train a Model:** Using the remaining features, train a Ridge Regression model to predict `y`. Use `scikit-learn`'s `Ridge` with `alpha=1.0` and `fit_intercept=True`. 
3. **Evaluate the Model:** Compute the Mean Squared Error (MSE) of the predictions on the training data.
4. **Numerical Library Configuration:** To ensure reproducibility and prevent thread contention on our cluster, you must run your Python analysis script with the following environment variables set to strictly limit threading to 1:
   - `OMP_NUM_THREADS=1`
   - `OPENBLAS_NUM_THREADS=1`
   - `MKL_NUM_THREADS=1`
   - `VECLIB_MAXIMUM_THREADS=1`
   - `NUMEXPR_NUM_THREADS=1`
5. **Generate a Report:** Create a JSON file at `/home/user/analysis_report.json` containing the results. The JSON must exactly follow this schema:
   ```json
   {
     "dropped_features": ["list", "of", "dropped", "column", "names"],
     "mse": 0.1234,
     "model_weights": {
       "f1": 0.1234,
       "f3": -0.5678
     }
   }
   ```
   *Note: Round the `mse` and all `model_weights` to exactly 4 decimal places.*

You may install any Python packages you need (like `pandas` and `scikit-learn`) using pip.