You are a Machine Learning Engineer preparing a robust training pipeline. You have encountered a dataset where the features are highly collinear (near-singular), causing standard Ordinary Least Squares (OLS) regression to perform poorly due to high variance.

Your task is to write a reproducible Python script at `/home/user/pipeline.py` that quantifies this issue, optimizes a regularized model, and compares the models statistically.

Here are the exact steps your script must perform:
1. Load the dataset from `/home/user/X.csv` (features) and `/home/user/y.csv` (targets). Both have headers and are comma-separated.
2. Calculate the condition number of the matrix $X^T X$ using `numpy.linalg.cond`. Save this single floating-point number to `/home/user/condition.txt`.
3. Set up a 5-fold cross-validation scheme using `sklearn.model_selection.KFold` with `n_splits=5`, `shuffle=True`, and `random_state=123`.
4. Iterate over the following candidate $\alpha$ (alpha) values for Ridge regression: `[0.001, 0.01, 0.1, 1.0, 10.0, 100.0]`.
5. For each fold, train an OLS model (`sklearn.linear_model.LinearRegression`) and a Ridge model (`sklearn.linear_model.Ridge`) for each candidate $\alpha$. Calculate the Mean Squared Error (MSE) on the validation fold.
6. Find the `optimal_alpha` that yields the lowest mean MSE across the 5 folds for Ridge regression.
7. Conduct a paired t-test (`scipy.stats.ttest_rel`) comparing the 5 validation MSEs of the OLS model against the 5 validation MSEs of the Ridge model trained with the `optimal_alpha`.
8. Save the results as a JSON file to `/home/user/results.json` with the following exact keys:
   - `"optimal_alpha"`: The best alpha value (float).
   - `"ols_mean_mse"`: The mean MSE of the OLS model across the 5 folds (float).
   - `"ridge_mean_mse"`: The mean MSE of the Ridge model with the optimal alpha across the 5 folds (float).
   - `"p_value"`: The p-value from the paired t-test comparing the OLS MSEs and optimal Ridge MSEs (float).

You must write and execute this script to generate `/home/user/condition.txt` and `/home/user/results.json`. Ensure the environment relies on standard Python data science libraries (numpy, pandas, scikit-learn, scipy).