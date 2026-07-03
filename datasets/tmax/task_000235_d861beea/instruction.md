You are acting as a performance engineer who needs to profile and analyze the response times of a critical microservice based on system metrics. 

You have been provided with a raw CSV log file at `/home/user/perf_data.csv`. The file contains 1000 rows of observational data with the following columns: `timestamp, cpu_util, mem_util, io_wait, response_time`.

Your goal is to build a Bayesian linear regression model to explain `response_time` based on the system metrics:
`response_time = b0 + b1*cpu_util + b2*mem_util + b3*io_wait + error`

You must implement the analysis in C. Write a C program at `/home/user/perf_model.c` that performs the following steps:

1. **Observational Data Reshaping**: Parse the CSV file and construct a design matrix $X$ (adding a column of 1s for the intercept `b0`) and a response vector $y$.
2. **Matrix Decomposition (Baseline)**: Use the LAPACKE library (you will need to install it and link against it, e.g., `-llapacke`) to compute the Ordinary Least Squares (OLS) estimate of the coefficients using QR decomposition or solving the normal equations (e.g., using `LAPACKE_dgels` or `LAPACKE_dposv`).
3. **MCMC Sampling & Posterior Estimation**: Implement a simple Metropolis-Hastings Random Walk MCMC sampler in C to estimate the posterior distribution of the coefficients $(b0, b1, b2, b3)$. 
   - Assume a flat prior for the coefficients and a Gaussian likelihood with a fixed standard deviation $\sigma = 1.0$.
   - Initialize the Markov chain at the OLS estimates.
   - Use a Gaussian proposal distribution with a standard deviation of 0.05 for each coefficient. (You can use standard standard library `rand()` based Box-Muller transform for normal random variables).
   - Run the chain for 50,000 iterations.
   - Discard the first 10,000 iterations as burn-in.
   - Calculate the mean of the posterior samples for the remaining 40,000 iterations.

4. **Output Logging**: Write the results to `/home/user/perf_analysis.log`. The file MUST contain exactly two lines in the following format (space-separated, floating point values printed to 4 decimal places):
```
OLS_COEFS: <b0> <b1> <b2> <b3>
MCMC_MEANS: <b0> <b1> <b2> <b3>
```

**Requirements:**
- Ensure you install any necessary C development libraries (like `liblapacke-dev`).
- The C program must be compiled to an executable named `/home/user/perf_model`.
- Run the executable to produce the log file.
- Because the MCMC is initialized at the OLS estimate and the likelihood is Gaussian with flat priors, the `MCMC_MEANS` should closely match the `OLS_COEFS`.