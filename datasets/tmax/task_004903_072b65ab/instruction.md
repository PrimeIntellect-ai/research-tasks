You are an AI assistant acting as a Data Engineer. You've inherited an ETL and modeling script that evaluates a machine learning model. However, you suspect there is a critical flaw: data leakage during the preprocessing steps (imputation and scaling).

Your task is to:
1. Review the existing script at `/home/user/etl_pipeline.py`. It currently reads data from `/home/user/data.csv`, applies global imputation and scaling (causing data leakage), and calculates the 10-fold cross-validated ROC AUC score.
2. Fix the data leakage by creating a proper Scikit-Learn `Pipeline` that correctly chains the `SimpleImputer` (with `strategy='mean'`), `StandardScaler`, and `LogisticRegression` (with `random_state=42`).
3. Compute the 10-fold cross-validated ROC AUC scores for this **corrected** pipeline using the exact same `KFold` cross-validator instance (`cv=KFold(n_splits=10, shuffle=True, random_state=42)`) as the flawed model.
4. Perform a paired t-test (using `scipy.stats.ttest_rel`) to compare the 10 CV scores of the flawed pipeline against the 10 CV scores of the corrected pipeline.
5. Save the results to a JSON file at `/home/user/results.json` with the following keys:
   - `"flawed_mean_auc"`: (float) The mean ROC AUC of the flawed approach.
   - `"corrected_mean_auc"`: (float) The mean ROC AUC of the corrected pipeline.
   - `"p_value"`: (float) The p-value from the paired t-test (two-sided).

Requirements:
- Do not modify the data generation or the initial loading steps.
- Do not change the random states or CV splitting strategy.
- Your final output must be exactly formatted in `/home/user/results.json`.
- Install any missing python libraries (e.g. `scikit-learn`, `pandas`, `scipy`) if needed.