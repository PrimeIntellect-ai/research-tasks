You are a Machine Learning Engineer preparing training data on a headless Linux server. You originally wrote a matplotlib script to visually inspect feature correlations, but due to a backend misconfiguration, it only produces blank plots. 

You need to switch to a purely statistical pipeline to select features and establish a baseline model.

A dataset has been provided at `/home/user/dataset.csv`. It contains 50 continuous features named `f1` through `f50`, and a continuous target variable named `target`.

Write a Python script to perform the following data preparation and baseline modeling tasks:

1. **Correlation and Hypothesis Testing**: 
   Iterate through all 50 features. For each feature, compute the Pearson correlation coefficient with the `target` variable and the associated p-value (testing the null hypothesis that there is no correlation).
   Keep only the features that satisfy BOTH of the following conditions:
   - The absolute value of the Pearson correlation coefficient is strictly greater than `0.2`.
   - The p-value is strictly less than `0.05`.

2. **Cross-Validation and Hyperparameter Tuning**:
   Using ONLY the features selected in step 1, train a `Ridge` regression model from `scikit-learn`. 
   Perform a grid search using 5-fold cross-validation (`GridSearchCV` with `cv=5`) to tune the regularization parameter `alpha`. 
   Test the following `alpha` values: `[0.1, 1.0, 10.0]`. 
   Use the default scoring metric (R^2). Set `random_state=42` if/where applicable for model reproducibility, though Ridge has an exact solution.

3. **Reporting**:
   Your script must output a JSON file at `/home/user/results.json` containing exactly the following keys:
   - `"selected_features"`: A list of strings containing the names of the features that passed the filter, sorted in alphabetical order.
   - `"best_alpha"`: A float representing the best `alpha` value found by the grid search.
   - `"best_cv_score"`: A float representing the best mean cross-validated score (`best_score_` from GridSearchCV), rounded to exactly 4 decimal places.

Ensure your script is self-contained, reads the dataset from the exact path specified, and outputs the JSON file exactly as requested.