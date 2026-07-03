You are tasked with building a Go-based performance benchmark and numerical accuracy test for a Bayesian inference algorithm. 

As a data analyst, you have been given a dataset at `/home/user/data.csv` containing two columns: `X` and `Y`. We want to model the relationship using linear regression: $Y_i \sim \mathcal{N}(\alpha + \beta X_i, \sigma^2)$, assuming $\sigma^2$ is fixed at $1.0$.

Your task is to write a Go program (`/home/user/mcmc.go`) that performs the following steps:
1. **Data Parsing:** Read `/home/user/data.csv` (has headers `X` and `Y`).
2. **Exact OLS (Numerical Baseline):** Calculate the Ordinary Least Squares (OLS) estimates for the intercept ($\alpha$) and slope ($\beta$) to serve as your exact numerical baseline.
3. **Bayesian Inference:** Implement a Random Walk Metropolis-Hastings MCMC sampler to estimate $\alpha$ and $\beta$. 
    - Set the random seed to `42` (`rand.Seed(42)` or `rand.New(rand.NewSource(42))`).
    - Number of iterations: 100,000.
    - Proposal distributions: $\alpha_{new} \sim \mathcal{N}(\alpha_{old}, 0.1^2)$ and $\beta_{new} \sim \mathcal{N}(\beta_{old}, 0.1^2)$.
    - Priors: Uniform over $[-100, 100]$ for both parameters.
    - Burn-in: Discard the first 10,000 iterations when computing the posterior mean.
    - Initial state: $\alpha=0.0$, $\beta=0.0$.
4. **Performance Benchmarking:** Measure the wall-clock execution time (in seconds) of just the MCMC loop (excluding I/O and OLS steps).
5. **Accuracy Testing:** Check if the MCMC posterior means for $\alpha$ and $\beta$ are within $0.05$ of the exact OLS estimates.
6. **Reporting:** The program must generate a JSON file at `/home/user/results.json` strictly matching this schema:
    ```json
    {
      "ols_alpha": 0.000,
      "ols_beta": 0.000,
      "mcmc_alpha": 0.000,
      "mcmc_beta": 0.000,
      "accuracy_pass": true,
      "mcmc_time_seconds": 0.000
    }
    ```
    Where `accuracy_pass` is a boolean (`true` if both MCMC estimates are within 0.05 of their OLS counterparts, `false` otherwise).

To complete the task, you must successfully write the code, compile/run it, and ensure `/home/user/results.json` is generated correctly.