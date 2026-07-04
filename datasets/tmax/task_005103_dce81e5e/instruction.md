You are a data analyst setting up an automated pipeline. You have a dataset at `/home/user/data/input.csv` with some missing and dirty data. Because your pipeline needs strict typing and fast execution, you must write a tool in Rust that parses the data, imputes missing values, and performs Multiple Linear Regression.

Your tasks:
1. Create a Rust project in `/home/user/ols_pipeline`.
2. The dataset at `/home/user/data/input.csv` has three columns: `x1`, `x2`, and `y`. It contains missing data represented as empty strings, `"NA"`, or `"NaN"`.
3. Your Rust program must read this file, parse the features and target as 64-bit floats (`f64`).
4. **Data Imputation**: For any missing or unparseable values in the feature columns (`x1`, `x2`), impute them using the arithmetic mean of the *valid* `f64` values in that specific column.
5. **Regression Calculation**: Using the imputed dataset, perform Multiple Linear Regression using Ordinary Least Squares (OLS) via the Normal Equation: $w = (X^T X)^{-1} X^T y$. You must use the `nalgebra` crate for matrix operations. 
6. Ensure you add an intercept term. This means your design matrix $X$ should have a column of `1.0`s as the first column (i.e., feature $x_0$), followed by the `x1` and `x2` columns.
7. Write the resulting coefficients (intercept, $w_1$, $w_2$) to `/home/user/output/coefficients.txt`. Each coefficient should be on a new line, printed to exactly 4 decimal places (e.g., `2.0000`).

Create the `data` and `output` directories if they do not exist, and write the appropriate code to pass this objective.