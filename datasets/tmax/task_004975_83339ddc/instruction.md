You are tasked with helping a data scientist fix a linear modeling pipeline in C++. 

The data scientist has a dataset `/home/user/data.csv` (100 rows, 4 columns: `X1, X2, X3, Y`). The features `X1` and `X2` are highly correlated, making the design matrix near-singular. The current C++ script, which attempts to find the weights using Ordinary Least Squares via Eigen's Cholesky decomposition, produces unstable results or fails entirely.

Your goal is to replace the failing OLS approach with a Bayesian approach using Markov Chain Monte Carlo (MCMC) sampling.

Requirements:
1. Ensure the C++ environment is set up. You will need the `Eigen3` library to handle matrix operations.
2. Write a C++ program (e.g., `/home/user/mcmc_sampler.cpp`) that reads `data.csv`.
3. The model is a Bayesian Linear Regression: $Y \sim \mathcal{N}(X\beta, \sigma^2 I)$, with a known observation variance $\sigma^2 = 1.0$.
4. Use a zero-mean Gaussian prior on the weights: $\beta \sim \mathcal{N}(0, \alpha^{-1} I)$, with precision $\alpha = 10.0$ (which acts as Ridge regularization).
5. Implement a Random Walk Metropolis-Hastings MCMC sampler to sample from the posterior of $\beta = [\beta_1, \beta_2, \beta_3]^T$.
    - Use a multivariate Gaussian proposal distribution centered at the current state with a covariance of $0.01 I$.
    - Initialize the chain at $\beta = [0, 0, 0]^T$.
    - Run the chain for a total of 15,000 iterations. Discard the first 5,000 iterations as burn-in.
6. Save the remaining 10,000 samples to `/home/user/samples.csv`. The file should contain exactly 10,000 lines, each with 3 comma-separated float values corresponding to the sampled $\beta_1, \beta_2, \beta_3$.

Compile your code with `g++ -O3 -I /usr/include/eigen3 mcmc_sampler.cpp -o mcmc_sampler` and run it. We will evaluate your work by analyzing the statistical properties of the samples in `/home/user/samples.csv`.