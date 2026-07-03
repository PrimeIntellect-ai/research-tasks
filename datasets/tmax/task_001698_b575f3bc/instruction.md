You are a Machine Learning Engineer tasked with preparing training data and building a fast surrogate model to replace a slow, legacy black-box scoring oracle.

You have been provided with an unlabeled dataset at `/app/data/unlabeled_features.csv`. It contains 10,000 rows and 20 continuous feature columns named `f0` through `f19`.
There is also a legacy scoring tool located at `/app/bin/scorer`. This is a stripped binary that takes the path to a CSV file (with the same 20 feature columns, no header) as its first command-line argument and prints the resulting scores to standard output (one float per line).

Because the legacy scorer is computationally expensive to run in production, you must build a lightweight Linear Regression surrogate model. However, you have a strict "compute budget" and may only query the legacy scorer for a randomly sampled subset of exactly 500 rows from the dataset.

Your workflow must be as follows:
1. Setup your environment by installing any necessary Python packages (e.g., `pandas`, `numpy`, `scipy`, `scikit-learn`).
2. Randomly sample exactly 500 rows from `/app/data/unlabeled_features.csv`. Query the `/app/bin/scorer` to get their target scores.
3. To perform feature selection rigorously, calculate the Pearson correlation coefficient between each feature and the target score. Use empirical bootstrap resampling (with N=1000 iterations) on your 500-row sample to compute the 95% confidence interval for the correlation coefficient of each feature.
4. Track your experiments: Save a JSON file at `/home/user/feature_correlations.json` containing the bootstrap confidence intervals. The keys should be the feature names (`f0`, `f1`, etc.), and the values should be a dictionary with `lower_bound` and `upper_bound`.
5. Select only the features whose 95% bootstrap confidence interval strictly does NOT contain 0 (i.e., statistically significant correlation).
6. Prepare your final training data using ONLY the selected features and the 500 sampled rows.
7. Train a standard `LinearRegression` model from `scikit-learn` on this prepared training data. Your model must accept input arrays containing only the selected features, arranged in ascending order of their original indices (e.g., if you select f5 and f2, the model input should have f2 as the first column and f5 as the second).
8. Save the trained model to `/home/user/surrogate_model.pkl` using the `joblib` library.

The automated verification system will load your `surrogate_model.pkl` and evaluate its R-squared ($R^2$) score against the true legacy scorer on a large, hidden test dataset. You must achieve an $R^2 \ge 0.90$.