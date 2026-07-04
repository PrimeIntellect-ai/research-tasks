You are a data scientist tasked with building and testing a new statistical modeling pipeline in Go.

Your objectives:
1. **Compile from source**: There is a C program provided at `/home/user/datagen.c` that generates a synthetic dataset. Compile it to an executable named `datagen` and run it. It will produce `/home/user/dataset.csv` with columns `y, x1, x2`.
2. **Matrix Decomposition & Modeling**: Write a Go program at `/home/user/solver.go` that reads `dataset.csv`. You must compute the Ordinary Least Squares (OLS) estimates for the multiple linear regression model $y = \beta_0 + \beta_1 x_1 + \beta_2 x_2$.
   - **Crucial Requirement**: You must solve the normal equations $X^T X \beta = X^T y$ by applying the **Cholesky decomposition** to $X^T X$. Do not use a pre-packaged OLS solver or QR decomposition directly on $X$. You may use `gonum.org/v1/gonum/mat` for matrix operations.
3. **Statistical Hypothesis Comparison**: In your Go program, compute the F-statistic to test the overall significance of the model (comparing the full model against an intercept-only null model).
   - $F = \frac{(SS_{tot} - SS_{res}) / p}{SS_{res} / (n - p - 1)}$, where $p$ is the number of predictors (excluding the intercept) and $n$ is the number of observations.
4. **Analytical Validation**: The true coefficients used in the data generator are approximately $\beta_0=2.5, \beta_1=-1.5, \beta_2=3.0$. Your Go code should include a basic regression test that asserts the estimated coefficients are within $0.05$ of these expected values.
5. **Output**: Your Go program must save the final computed values to `/home/user/results.json` in the following exact format:
```json
{
  "beta0": 2.4667,
  "beta1": -1.5000,
  "beta2": 3.0000,
  "f_stat": 12345.6789
}
```
Round the values to exactly 4 decimal places.

Initialize your Go module with `go mod init solver` in `/home/user`.
Execute your Go program and ensure `/home/user/results.json` is created successfully.