You are a data scientist tasked with cleaning a messy dataset using statistical and linear algebraic methods, testing the effect of your cleaning, and building a baseline model. 

The raw data is located at `/home/user/raw_data.csv`. It contains 5 feature columns (`f1`, `f2`, `f3`, `f4`, `f5`) and one target column (`y`). 

Write a Python script at `/home/user/clean_and_tune.py` that performs the following steps and outputs the results to a JSON file.

**Step 1: Linear Algebra Outlier Removal**
1. Extract the feature matrix $X$ (columns `f1` to `f5`).
2. Calculate the sample mean vector and the empirical covariance matrix of $X$.
3. Compute the Mahalanobis distance for each sample in the dataset using the covariance matrix. 
4. Remove all samples (rows) where the Mahalanobis distance is strictly greater than `15.0`. This yields the "cleaned" dataset.

**Step 2: Hypothesis Testing & Confidence Intervals**
1. Evaluate the impact of the outlier removal on the target variable.
2. Perform a two-sided, two-sample independent t-test (Welch's t-test, assuming unequal variances) comparing the `y` values of the **original** dataset against the `y` values of the **cleaned** dataset.
3. Calculate the 95% confidence interval for the difference in means $(\mu_{original} - \mu_{cleaned})$. *Hint: Use `scipy.stats.ttest_ind(..., equal_var=False)` which has a `confidence_interval()` method in newer SciPy versions. You may need to upgrade `scipy` using pip.*

**Step 3: Cross-Validation & Hyperparameter Tuning**
1. Using ONLY the **cleaned** dataset, train a `Ridge` regression model to predict `y` from the features `f1` to `f5`.
2. Use `sklearn.model_selection.GridSearchCV` with 5-fold cross-validation to find the optimal regularization strength `alpha`.
3. Search over the exact following grid for `alpha`: `[0.01, 0.1, 1.0, 10.0, 100.0]`.
4. Use negative mean squared error (`neg_mean_squared_error`) as the scoring metric. Random states or shuffling are not necessary for this standard CV unless specified.

**Step 4: Output**
Save your final results to `/home/user/results.json` with the exact following keys:
- `"outliers_removed"`: (integer) The number of rows removed during Step 1.
- `"t_statistic"`: (float) The test statistic from the t-test, rounded to 4 decimal places.
- `"p_value"`: (float) The p-value from the t-test, rounded to 4 decimal places.
- `"ci_lower"`: (float) The lower bound of the 95% confidence interval, rounded to 4 decimal places.
- `"ci_upper"`: (float) The upper bound of the 95% confidence interval, rounded to 4 decimal places.
- `"best_alpha"`: (float) The best `alpha` value found by GridSearchCV.

Your solution should be executable via `python3 /home/user/clean_and_tune.py`. You may install necessary packages (like `pandas`, `numpy`, `scipy`, `scikit-learn`) using pip.