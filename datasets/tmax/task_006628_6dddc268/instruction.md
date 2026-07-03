You are helping a researcher organize and analyze a dataset of paired measurements. The data is located at `/home/user/data.csv` and contains 100 rows with two comma-separated numeric columns, representing variables X and Y. There is no header row.

Your task is to write a C program that performs a simple statistical analysis and Bayesian update. 

1. Write a C program and save it to `/home/user/analyze.c`.
2. The program must read `/home/user/data.csv`.
3. Compute the sample covariance between X and Y. Use the unbiased estimator (divide by N-1).
4. Compute the Bayesian posterior mean of X. Assume:
   - The prior distribution of the mean of X is Normal with $\mu_0 = 5.0$ and variance $\sigma_0^2 = 2.0$.
   - The measurements of X are normally distributed with an assumed known variance $\sigma^2 = 3.0$.
   - The N measurements are independent.
5. The C program must write the results to `/home/user/results.txt` in exactly the following format (values rounded to 4 decimal places):
```
Covariance: [your_covariance_value]
Posterior Mean: [your_posterior_mean_value]
```
6. Install a C compiler if one isn't available, compile your code, and run it to produce the `results.txt` file.