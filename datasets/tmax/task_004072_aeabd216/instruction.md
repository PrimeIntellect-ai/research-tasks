You are acting as a computational statistics researcher. We need to build a reproducible C++ pipeline to estimate the posterior distribution of a parameter $\mu$ using both optimization (Gradient Ascent) and Markov Chain Monte Carlo (MCMC). 

You must write a C++ program and a bash script to automate the build and execution process. 

**Model Specification:**
1. **Prior:** The prior for $\mu$ is a normal distribution $\mathcal{N}(0, 100)$. (Mean=0, Variance=100)
2. **Likelihood:** We have $N=50$ data points drawn from $\mathcal{N}(\mu, 1)$. (Variance is fixed at 1).
3. **Log-Posterior:** Up to an additive constant, the log-posterior is $L(\mu) = -\frac{\mu^2}{200} - \sum_{i=1}^{50} \frac{(x_i - \mu)^2}{2}$.

**Your objectives:**

1. **Write the C++ source code `/home/user/posterior_estimation.cpp`:**
    *   **Data Generation:** Initialize a `std::mt19937` RNG with seed `42`. Draw $N=50$ data points $x_i$ from `std::normal_distribution<double>(5.0, 1.0)`. *Important: Keep this exact RNG instance for the rest of the program to ensure reproducibility.*
    *   **Optimization (Gradient Ascent):** Start with an initial guess of $\mu = 0.0$. Perform 100 iterations of gradient ascent to maximize $L(\mu)$. Use a learning rate of $0.01$. The analytic derivative of $L(\mu)$ is $L'(\mu) = -\frac{\mu}{100} + \sum_{i=1}^{50} (x_i - \mu)$. Let the final value be `MAP_MU`.
    *   **MCMC (Metropolis-Hastings):** Using the *same* RNG instance, run a Metropolis-Hastings sampler for 100,000 iterations to sample from the posterior proportional to $\exp(L(\mu))$. 
        *   Start the chain at $\mu_{curr} = 0.0$.
        *   In each iteration, propose a new state $\mu_{prop} \sim \mathcal{N}(\mu_{curr}, 0.5^2)$.
        *   Calculate the acceptance probability $\alpha = \min(1.0, \exp(L(\mu_{prop}) - L(\mu_{curr})))$.
        *   Draw $u \sim \text{Uniform}(0, 1)$. If $u < \alpha$, accept the proposal ($\mu_{curr} = \mu_{prop}$).
        *   Store the samples.
    *   **Convergence & Estimation:** Discard the first 50,000 samples as burn-in. Using the remaining 50,000 samples, calculate the empirical mean (`MCMC_MEAN`) and empirical variance (`MCMC_VAR`).
    *   **Output:** The program should write exactly three lines to `/home/user/results.txt`:
        ```
        MAP_MU: <value>
        MCMC_MEAN: <value>
        MCMC_VAR: <value>
        ```

2. **Write a bash script `/home/user/run_pipeline.sh`:**
    *   This script must compile the C++ code using `g++` (require C++17, output binary named `sampler`).
    *   It must execute the binary.
    *   Make sure the script is executable.

Run your bash script to produce the final `results.txt` file. Ensure your math, particularly the variance calculation and the acceptance ratio, is completely accurate.