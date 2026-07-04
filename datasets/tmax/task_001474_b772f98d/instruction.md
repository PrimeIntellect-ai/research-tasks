You are a machine learning engineer preparing a training dataset. The raw feature data is heavily correlated, and you need to "whiten" the features (decorrelate them and scale them to unit variance) before fitting a regression model.

Your task is to write a Rust program that performs multivariate density estimation, Cholesky decomposition-based whitening, and regression via LU decomposition.

I have created a skeleton Rust project at `/home/user/ml_prep`. 
There is a dataset at `/home/user/ml_prep/data.csv` without headers. The first 3 columns are the features ($X$), and the 4th column is the target variable ($y$). There are exactly 100 rows.

Write a Rust program in `/home/user/ml_prep/src/main.rs` that does the following:
1. **Density Estimation:** Calculate the empirical mean vector $\mu$ (length 3) and the Maximum Likelihood (population) covariance matrix $\Sigma$ (3x3) of the features $X$. Use $N$ (not $N-1$) in the covariance denominator.
2. **Matrix Decomposition:** Perform a Cholesky decomposition of the covariance matrix such that $\Sigma = L L^T$, where $L$ is the lower triangular matrix.
3. **Whitening:** Transform each feature vector $x^{(i)}$ to a whitened vector $w^{(i)}$ using the formula: $w^{(i)} = L^{-1} (x^{(i)} - \mu)$. Let $W$ be the $100 \times 3$ matrix of these whitened features.
4. **Curve Fitting/Regression:** Fit a linear regression model $y = W \beta$ (without an intercept term) using the Normal Equations ($W^T W \beta = W^T y$). Solve this linear system for the coefficients $\beta$ strictly by using LU decomposition.
5. **Convergence/Error Testing:** Calculate the Mean Squared Error (MSE) of the predictions $\hat{y} = W \beta$ compared to the true $y$.

Your program must output a JSON file at `/home/user/ml_prep/results.json` with the exact following structure and keys:
```json
{
  "mean": [mu_0, mu_1, mu_2],
  "cholesky_lower": [
    [L_00, L_01, L_02],
    [L_10, L_11, L_12],
    [L_20, L_21, L_22]
  ],
  "regression_coeffs": [beta_0, beta_1, beta_2],
  "mse": 0.00000
}
```

Constraints:
- You must use the `nalgebra` crate for matrix operations. 
- You may add necessary crates (like `csv`, `serde_json`) to `Cargo.toml`.
- Run your program to generate the `results.json` file.