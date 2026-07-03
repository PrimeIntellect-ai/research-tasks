You are acting as a data scientist fitting a Bayesian linear regression model. You have a dataset located at `/home/user/data.csv` containing 100 observations. The file has three columns: `x1`, `x2`, and `y`. You are modeling this as $y_i = \beta_0 + \beta_1 x_{i1} + \beta_2 x_{i2} + \epsilon_i$, where $\epsilon_i \sim N(0, 1)$.

Your task is to write a C program (`/home/user/fit_model.c`) that does the following without relying on external mathematical libraries other than the standard C math library (`<math.h>`):

1. **Analytical Solution Validation:** Compute the exact Ordinary Least Squares (OLS) solution $\hat{\beta} = (X^T X)^{-1} X^T y$. To do this, explicitly construct the $3 \times 3$ matrix $X^T X$ (remembering the intercept term for $\beta_0$) and implement a matrix decomposition method (e.g., Cholesky, LU, or Cramer's rule) to solve for $\beta$.
2. **MCMC Sampling:** Implement a Random Walk Metropolis-Hastings MCMC sampler to estimate the posterior means of $\beta_0, \beta_1, \beta_2$. 
   - Use a Gaussian prior for $\beta$ centered at 0 with variance 100.
   - Use a spherical Gaussian proposal distribution with a standard deviation of 0.05 for each parameter.
   - Run the MCMC for 500,000 iterations, discarding the first 10,000 as burn-in. (You can use the standard `rand()` for uniform generation and Box-Muller for normals. Seed your random number generator with `srand(42)`).
3. **Reference Dataset Comparison:** Your C program should write two output files:
   - `/home/user/analytical_results.txt`: A single line containing the exact $\beta_0, \beta_1, \beta_2$ separated by commas, formatted to 3 decimal places (e.g., `1.234,2.345,3.456`).
   - `/home/user/mcmc_results.txt`: A single line containing the MCMC posterior means of $\beta_0, \beta_1, \beta_2$ separated by commas, formatted to 3 decimal places.

Compile and run your C program to produce these two files. The MCMC results should closely approximate the analytical results.