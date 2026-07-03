You are a data scientist working on an analysis where the input features are highly collinear, causing standard Ordinary Least Squares (OLS) estimates to become extremely unstable (an ill-conditioned/near-singular design matrix).

Your objective is to fit a robust model and estimate the uncertainty of its parameters using a bootstrap approach.

Dataset location: `/home/user/experiment.csv`
Columns: `x1`, `x2`, `x3`, `y`

Please perform the following steps:
1. Fit a Ridge Regression model to predict `y` using `x1`, `x2`, and `x3`. Use a regularization strength (often denoted as alpha or lambda) of `2.0`. Do NOT fit an intercept (assume the data is already centered or forces the intercept to 0).
2. To quantify the uncertainty of the coefficient for `x1` under these collinear conditions, perform a Bootstrap analysis.
3. Draw exactly `10000` bootstrap samples. Each sample should be created by sampling rows from the original dataset with replacement (each sample must have the same number of rows as the original dataset).
4. For each bootstrap sample, fit the Ridge regression model (alpha=2.0, no intercept) and record the coefficient for `x1`.
5. Calculate the mean, the 2.5th percentile (lower bound of the 95% Confidence Interval), and the 97.5th percentile (upper bound of the 95% Confidence Interval) of the `x1` coefficients across all 10,000 bootstrap iterations.

Write your final summary to `/home/user/ci_results.json` in the following exact JSON format:
```json
{
  "mean": <float>,
  "lower_bound": <float>,
  "upper_bound": <float>
}
```

You may use any programming language (Python, R, Julia, etc.) available in a standard scientific computing environment. Do not round your intermediate calculations, and write the final JSON values out to at least 4 decimal places.