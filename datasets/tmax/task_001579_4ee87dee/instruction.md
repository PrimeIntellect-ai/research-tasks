You are an ETL Data Engineer. You have been tasked with building a C++ data processing pipeline that handles missing data imputation and performs hyperparameter tuning for a downstream linear algebra model.

You are provided with a raw dataset at `/home/user/dataset.csv`. The dataset has the following columns: `id,f1,f2,y`. 
- `id` is an integer.
- `f1`, `f2`, and `y` are continuous variables. 
- `f1` and `f2` contain missing values represented by the string `"NaN"`.

Unfortunately, earlier iterations of this pipeline in Python (pandas) suffered from a bug where integer IDs were silently cast to floats and lost precision when NaNs were introduced. You must build a robust C++ pipeline that avoids this.

Write and execute a C++ program at `/home/user/pipeline.cpp` that does the following:
1. **ETL & Imputation:** Read the CSV file. Parse `id` as an exact integer, and `f1, f2, y` as double-precision floats. Impute any `"NaN"` values in `f1` and `f2` using the mean of the *observed* (non-NaN) values in their respective columns.
2. **Cross-Validation & Hyperparameter Tuning:** Using the cleaned data, perform 5-fold cross-validation to tune the regularization parameter $\lambda$ for a Ridge Regression model (without an intercept/bias term). 
   - The model formula is: $\beta = (X^T X + \lambda I)^{-1} X^T y$, where $X$ is the feature matrix `[f1, f2]`.
   - Use sequential folds without shuffling (i.e., if there are 100 rows, Fold 1 uses rows 0-19 as validation and 20-99 as training, Fold 2 uses 20-39 as validation, etc.).
   - Evaluate $\lambda$ values in the set: `{0.1, 1.0, 10.0}`.
   - Calculate the Mean Squared Error (MSE) for each fold.
3. **Outputs:** 
   - Save the fully imputed dataset to `/home/user/clean_data.csv` in the format `id,f1,f2,y`. Format the doubles to exactly 4 decimal places.
   - Determine the $\lambda$ that yields the lowest average MSE across the 5 folds and write this single numeric value to `/home/user/best_lambda.txt`.

You may use Eigen3 for the linear algebra calculations. Eigen3 headers are available at `/usr/include/eigen3` (you will need to compile your code with `-I/usr/include/eigen3`).