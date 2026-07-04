You are a Data Engineer building a data quality and prediction ETL pipeline. You need to write a Python script that analyzes incoming batch data against historical baselines to detect data drift and trains a predictive model to ensure data consistency.

Setup requirements:
1. Create a Python virtual environment at `/home/user/etl_env` and install `pandas`, `numpy`, `scikit-learn`, and `scipy`.
2. All your code should be written in a script located at `/home/user/pipeline/quality_check.py`.
3. Before running any mathematical operations in your script, configure numpy to raise an error on division by zero by adding `import numpy as np; np.seterr(divide='raise')`.
4. The data files are located at `/home/user/data/historical.csv` (training data) and `/home/user/data/batch_01.csv` (new incoming data). Both files have columns: `feature_1`, `feature_2`, `feature_3`, and `revenue`.

Your script `quality_check.py` must perform the following tasks sequentially:

**Phase 1: Hyperparameter Tuning & Cross Validation**
Use the historical data (`historical.csv`) to train a Ridge regression model predicting `revenue` from `feature_1`, `feature_2`, and `feature_3`.
- Use `sklearn.model_selection.GridSearchCV` with 5-fold cross-validation.
- Test the following `alpha` values: `[0.1, 1.0, 10.0, 100.0]`.
- Use the default scoring metric (R^2).
- Set `random_state=42` if/where applicable (Ridge regression does not strictly require it for standard dense solvers, but ensure no shuffling is done in CV or set shuffle=False which is default for KFold).

**Phase 2: Confidence Intervals**
Calculate the 95% confidence interval for the mean of the `revenue` column in the *new incoming data* (`batch_01.csv`).
- Use `scipy.stats.t.interval`. The degrees of freedom should be N-1. Use the sample mean and the standard error of the mean (`scipy.stats.sem`).

**Phase 3: Hypothesis Testing**
Perform Welch's t-test (independent t-test with unequal variances) to determine if the mean `revenue` of the incoming data significantly differs from the historical data.
- Use `scipy.stats.ttest_ind` with `equal_var=False`.
- The null hypothesis is that the means are equal. Flag `data_drift_detected` as `True` if the p-value is strictly less than `0.05`.

**Phase 4: Reporting**
Your script must output a JSON file at `/home/user/pipeline/report.json` containing exactly the following keys and typed values (round all floats to exactly 4 decimal places):
- `"best_alpha"`: (float) The best alpha value found during cross-validation.
- `"cv_best_score"`: (float) The best mean cross-validation score.
- `"new_revenue_mean_ci"`: (list of two floats) `[lower_bound, upper_bound]` representing the 95% CI.
- `"t_test_p_value"`: (float) The p-value from Welch's t-test.
- `"data_drift_detected"`: (boolean) `True` or `False`.

Run your pipeline script to generate the `report.json` file.