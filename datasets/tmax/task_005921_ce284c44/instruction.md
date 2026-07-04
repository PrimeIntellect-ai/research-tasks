You are an AI assistant helping a Machine Learning Engineer prepare a generative model and synthetic training data. We need to estimate the posterior of a parameter $\mu$ for a physical system using Approximate Bayesian Computation (ABC) via Markov Chain Monte Carlo (MCMC). 

The true observed data is stored in `/home/user/y_obs.csv` (100 float values, one per line).

The generative process for a proposed parameter $\mu$ is:
1. Draw 100 samples of $x$ from a Normal distribution $\mathcal{N}(\mu, 1.0)$.
2. For each $x$, the physical system produces an output $y$ which is the unique real root of the non-linear equation: $y^3 + y - x = 0$. Solve this using the Newton-Raphson method (or any equivalent root-finding algorithm) to an accuracy of at least $10^{-5}$.
3. This set of 100 $y$ values constitutes the simulated dataset $Y_{sim}(\mu)$.

To perform MCMC (Metropolis-Hastings), implement a Rust program in `/home/user/mcmc_solver` that does the following:
1. Initialize $\mu_0 = 0.0$.
2. For $i = 1$ to $5000$ (total iterations):
   a. Propose a new state $\mu_{prop} \sim \mathcal{N}(\mu_{i-1}, 0.5^2)$.
   b. Generate $Y_{sim}(\mu_{prop})$ following the generative process above.
   c. Compute the 1-Wasserstein distance between $Y_{sim}$ and $Y_{obs}$. In 1D, this is simply the mean absolute difference of the sorted arrays: $W = \frac{1}{100} \sum_{k=1}^{100} |Y_{sim, (k)} - Y_{obs, (k)}|$.
   d. Compute the acceptance probability $\alpha = \min(1, \exp(10 \times (W_{curr} - W_{prop})))$. (For $i=1$, $W_{curr}$ is the distance computed using $\mu_0=0.0$).
   e. Draw $u \sim \text{Uniform}(0, 1)$. If $u < \alpha$, accept the proposal ($\mu_i = \mu_{prop}$, $W_{curr} = W_{prop}$). Otherwise, reject ($\mu_i = \mu_{i-1}$).
3. Discard the first 1000 samples as burn-in.
4. Calculate the mean of the remaining 4000 samples of $\mu$.
5. Save this mean value as a string (formatted to 2 decimal places) in `/home/user/posterior_mean.txt`.

Requirements:
- Use **Rust** to build this tool. You can create a new cargo project. 
- You may use the `rand` and `rand_distr` crates.
- Execute the Rust program to generate the required output file.