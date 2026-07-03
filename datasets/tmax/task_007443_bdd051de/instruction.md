You are a machine learning engineer building a robust synthetic data generator. You need to estimate the parameters of a polynomial trend from a noisy seed dataset using Bayesian inference, starting from an Ordinary Least Squares (OLS) guess.

You have been provided a dataset at `/home/user/data.csv` containing 50 rows of `X,Y` coordinate pairs (comma-separated floats).

Your task is to write a C program, saved at `/home/user/fit_sampler.c`, that performs the following steps:

1. **Read the Data:** Load the 50 `X,Y` pairs from `/home/user/data.csv`.
2. **Matrix Setup for Polynomial Regression:** We are fitting a degree-2 polynomial: $Y = \beta_0 + \beta_1 X + \beta_2 X^2$. Construct the $50 \times 3$ Vandermonde design matrix $V$ and the response vector $Y$.
3. **QR Decomposition for Initial Estimate:** Use the GNU Scientific Library (GSL) to perform a QR decomposition of $V$ (`gsl_linalg_QR_decomp`) and solve for the least squares estimate of the coefficients (`gsl_linalg_QR_lssolve`). Let this be $\beta^{(ols)}$.
4. **Metropolis-Hastings MCMC Sampling:** 
   Use $\beta^{(ols)}$ as the initial state ($\beta^{(0)}$) for an MCMC chain to sample from the posterior of $\beta$.
   - **Likelihood:** Assume the data generation process is $Y_i \sim \mathcal{N}(\beta_0 + \beta_1 X_i + \beta_2 X_i^2, \sigma^2)$ with fixed noise standard deviation $\sigma = 1.0$.
   - **Prior:** Assume an improper flat prior for all $\beta$ coefficients (i.e., prior probability is constant and cancels out).
   - **Proposal Distribution:** For each step $t$ from $1$ to $10000$:
     - Propose a new state: $\beta^{(prop)}_j = \beta^{(t-1)}_j + \epsilon_j$, where $\epsilon_j \sim \mathcal{N}(0, 0.1^2)$ for $j \in \{0, 1, 2\}$.
     - **Crucial RNG Sequence for Reproducibility:** 
       Use the `gsl_rng_mt19937` generator initialized with seed `42` (`gsl_rng_set(r, 42)`).
       At the start of each of the 10,000 iterations, draw exactly four random numbers in this strict order:
       1. $\epsilon_0$: `gsl_ran_gaussian(r, 0.1)`
       2. $\epsilon_1$: `gsl_ran_gaussian(r, 0.1)`
       3. $\epsilon_2$: `gsl_ran_gaussian(r, 0.1)`
       4. $u$: `gsl_rng_uniform(r)` (used for the acceptance check: accept if $u < \text{acceptance\_ratio}$, otherwise reject. Use log-likelihoods to avoid underflow).
5. **Posterior Estimation:**
   Discard the first 1,000 iterations as burn-in. Calculate the mean of $\beta_0, \beta_1, \beta_2$ over the remaining 9,000 samples. Let this be $\beta^{(mcmc)}$.
6. **Output:** 
   Write the results to `/home/user/results.txt` in exactly the following format (formatted to 4 decimal places):
   ```
   OLS: beta0=..., beta1=..., beta2=...
   MCMC: beta0=..., beta1=..., beta2=...
   ```

**Constraints & Notes:**
- Standard Ubuntu libraries like `libgsl-dev` are available or can be installed via apt-get if necessary.
- Compile your program as needed (e.g., `gcc fit_sampler.c -o fit_sampler -lgsl -lgslcblas -lm`) and run it to produce the `results.txt` file.
- Do not modify the seed data.