You are an MLOps engineer tasked with fixing a broken experiment tracking pipeline and resolving a critical data leakage issue.

In the `/home/user/pipeline` directory, you will find:
1. `data.csv`: A dataset of user features and an engagement score.
2. `train.py`: A script that trains a Ridge Regression model to predict engagement, logs metrics to MLflow, and computes a correlation matrix.

However, the current pipeline has severe flaws:
1. **Data Leakage**: The script applies `SimpleImputer` and `StandardScaler` (`fit_transform`) on the *entire dataset* before performing the `train_test_split`.
2. **Missing Confidence Intervals**: The pipeline logs the Mean Squared Error (MSE) but lacks uncertainty estimation for the A/B test simulation.

Your tasks are:
1. **Start an MLflow Server**: Start a local MLflow tracking server running on `http://127.0.0.1:5000`. The backend store and artifact root should be stored in `/home/user/mlruns`. Run this as a background process.
2. **Fix Data Leakage**: Modify `/home/user/pipeline/train.py`. Ensure that the imputer and scaler are `fit` **only** on the training data, and then used to `transform` both the train and test sets.
3. **Fix Correlation Analysis**: The script computes a Pearson correlation matrix of the features. Update this to ensure the correlation matrix is computed **only** on the scaled training features (to avoid leaking test feature distributions).
4. **Add Confidence Intervals**: Calculate the 95% confidence interval for the test set Mean Squared Error. 
   - Compute the squared errors for each prediction in the test set.
   - Use `scipy.stats.t.interval` (or equivalent standard error of the mean logic for a t-distribution) on these squared errors to find the 95% CI of the MSE.
   - Log these values to MLflow as metrics: `mse_ci_lower` and `mse_ci_upper`.
5. **Execute and Report**: Run the fixed `train.py` script. After a successful run, query MLflow (via API or MLflow client) to get the ID of the run. Create a file at `/home/user/pipeline/fix_summary.json` with the following exact structure:
```json
{
  "run_id": "<your_mlflow_run_id>",
  "mse_ci_lower": 1.2345,
  "mse_ci_upper": 2.3456
}
```
Replace the values with your actual run ID and the calculated CI bounds (rounded to 4 decimal places).

Requirements:
- Python packages `mlflow`, `scikit-learn`, `pandas`, and `scipy` are available.
- Do not change the `RANDOM_STATE = 42` in `train.py` to ensure reproducibility.
- Do not change the model hyperparameters.