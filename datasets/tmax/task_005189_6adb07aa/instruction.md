You are tasked with fixing a data leakage issue in a machine learning script. 

There is a Python script located at `/home/user/model_pipeline.py`. It evaluates a model using cross-validation. However, there is a data leakage problem: feature selection (`SelectKBest`) is applied to the entire dataset *before* the cross-validation splits are made. This leaks information from the validation sets into the training sets, resulting in an artificially inflated $R^2$ score.

Your task is to:
1. Modify `/home/user/model_pipeline.py` to eliminate this data leakage.
2. Use a `sklearn.pipeline.Pipeline` to ensure that `SelectKBest` is fit only on the training folds during cross-validation.
3. Keep the same random seeds, model (`Ridge`), cross-validation strategy (`KFold` with 5 splits), and number of selected features (`k=10`).
4. Run the fixed script so that it outputs the corrected average $R^2$ score to `/home/user/metrics.json`.

Do not modify the data generation part of the script. The final `metrics.json` should contain the single key `mean_r2`.