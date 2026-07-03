You are an AI assistant helping a computational statistician fix a reproducibility and numerical stability issue in their MCMC pipeline.

The researcher is trying to sample from a 2D Multivariate Normal target distribution and measure how well the empirical sample matches the true distribution using Kullback-Leibler (KL) divergence. However, their current pipeline suffers from catastrophic cancellation in the covariance calculation and numerically unstable matrix inversions.

Your task is to write a reproducible C++ pipeline from scratch that performs the MCMC sampling, stably computes the empirical statistics, and calculates the probability distance metric.

**Task Requirements:**

1.  **Environment & Dependencies**:
    *   Install the `Eigen3` C++ library (using `apt-get` or similar).
    *   All your code should be written in `/home/user/mcmc_pipeline.cpp`.
    *   Compile it to `/home/user/mcmc_pipeline` using `g++` (ensure you link Eigen3 properly).

2.  **MCMC Sampling Specification**:
    *   Target Distribution $N(\mu, \Sigma)$: $\mu = [1.0, 2.0]^T$, $\Sigma = \begin{bmatrix} 2.0 & 0.5 \\ 0.5 & 1.0 \end{bmatrix}$.
    *   Algorithm: Random Walk Metropolis-Hastings.
    *   Proposal Distribution: $X_{new} \sim N(X_{old}, \Sigma_{prop})$, where $\Sigma_{prop} = \begin{bmatrix} 0.1 & 0 \\ 0 & 0.1 \end{bmatrix}$.
    *   Initialization: Start at $X_0 = [0.0, 0.0]^T$.
    *   Iterations: 10,000 burn-in steps, followed immediately by 100,000 sampling steps.
    *   Reproducibility: Use `std::mt19937` initialized with seed `42`. To avoid compiler-specific `std::normal_distribution` implementations, generate standard normal random variables using the exact Box-Muller transform applied to `std::uniform_real_distribution<double>(0.0, 1.0)`.

3.  **Numerical Stability Requirements**:
    *   **Matrix Decomposition**: To evaluate the log-density of the target distribution for the acceptance ratio, you **must** use Eigen's Cholesky Decomposition (`LLT`) to compute the determinant and the inverse action $\Sigma^{-1} (x-\mu)$ robustly. Do not use `.inverse()` or `.determinant()` directly on $\Sigma$.
    *   **Online Covariance**: To prevent catastrophic cancellation, you **must** compute the empirical mean ($\hat{\mu}$) and empirical covariance matrix ($\hat{\Sigma}$) of the 100,000 samples using **Welford's online algorithm** for multivariate data. Do not store all 100,000 samples in memory and do not use the naive $E[X^2] - E[X]^2$ formula.

4.  **Distribution Distance Metric**:
    *   Compute the Kullback-Leibler divergence $D_{KL}(N_{emp} || N_{target})$ from the empirical distribution $N_{emp}(\hat{\mu}, \hat{\Sigma})$ to the target distribution $N_{target}(\mu, \Sigma)$.
    *   Formula: $D_{KL}(N_0 || N_1) = \frac{1}{2} \left[ \log \frac{|\Sigma_1|}{|\Sigma_0|} - d + \text{tr}(\Sigma_1^{-1} \Sigma_0) + (\mu_1 - \mu_0)^T \Sigma_1^{-1} (\mu_1 - \mu_0) \right]$, where $d=2$.

5.  **Output Format**:
    *   Your C++ program must write a JSON file to `/home/user/results.json` containing the empirical statistics and the KL divergence.
    *   Format:
        ```json
        {
          "empirical_mu": [m1, m2],
          "empirical_cov": [[c11, c12], [c21, c22]],
          "kl_divergence": kl_val
        }
        ```
    *   The program should execute successfully when run as `/home/user/mcmc_pipeline`.

Make sure to execute your compilation step and run the binary so the `results.json` file is present.