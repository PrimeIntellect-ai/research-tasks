I need you to process a dataset and find the best regularization parameter for a Ridge Regression model. 

You will find a CSV file located at `/home/user/data.csv`. The file contains three columns: `f1`, `f2`, and `target`.

Please write and run a Python script to perform the following steps exactly in this order:
1. Load the dataset from `/home/user/data.csv`.
2. Remove any rows where the `target` value is strictly greater than 1000 (these are extreme outliers due to a sensor malfunction).
3. The column `f1` has some missing values. Impute these missing values using the median of the `f1` column (calculate the median *after* removing the outliers).
4. Using `scikit-learn`, fit a Ridge Regression model with Cross-Validation (`RidgeCV`) to predict `target` using `f1` and `f2` as features. Use the following alphas to test: `[0.1, 1.0, 10.0]`. Leave the other `RidgeCV` parameters as their defaults (which defaults to leave-one-out cross-validation).
5. Output the best performing alpha (the `best_alpha_` attribute) into a file named `/home/user/best_alpha.txt`. The file should contain nothing but the numerical value of the best alpha.

You may need to install standard data science libraries (like `pandas` and `scikit-learn`) using pip before writing and executing your script.