You are a bioinformatics analyst investigating potential hypermutation regions in a newly sequenced genome. You have a set of mutation counts observed across several 1kb sliding windows in a specific genomic region. 

Your task is to write a Rust program that uses Markov Chain Monte Carlo (MCMC) to estimate the posterior distribution of the mutation rate $\lambda$, test for convergence, and evaluate the hypothesis that this region is hypermutated compared to a known reference baseline.

Setup & Data:
1. The mutation counts are stored in `/home/user/data/counts.txt` (one integer per line).
2. The mutations in these windows are modeled as independent Poisson random variables with an unknown rate parameter $\lambda$.
3. Use a Gamma prior for $\lambda$ with shape parameter $\alpha = 2.0$ and rate parameter $\beta = 1.0$.
4. The reference baseline mutation rate is $\lambda_0 = 2.5$. The region is considered "hypermutated" if the posterior mean of $\lambda$ is strictly greater than $\lambda_0$.

Instructions:
1. Initialize a new Rust binary project at `/home/user/mcmc_mutations`. You may use the `rand` and `rand_distr` crates.
2. Implement a Metropolis-Hastings MCMC sampler in Rust to draw samples from the posterior distribution of $\lambda$. 
    - Proposal distribution: Normal distribution centered at the current $\lambda$ with standard deviation $\sigma = 0.5$. (Reject proposals where $\lambda_{new} \le 0$).
    - Run the chain for $10,000$ iterations.
    - Discard the first $1,000$ iterations as burn-in.
3. Calculate the posterior mean of $\lambda$ from the remaining $9,000$ samples.
4. Calculate the acceptance rate of the MCMC chain (over all 10,000 proposals).
5. Compare the posterior mean to the reference $\lambda_0 = 2.5$ to test the hypermutation hypothesis.
6. Output your results to a JSON file at `/home/user/results.json` with exactly the following keys:
    - `"posterior_mean"`: The computed posterior mean (float).
    - `"acceptance_rate"`: The fraction of proposed MCMC steps that were accepted (float).
    - `"hypermutated"`: A boolean indicating whether the posterior mean is greater than $2.5$.

Execute your Rust program so that the `/home/user/results.json` file is generated. Ensure your MCMC implementation is mathematically sound according to the log-likelihood of the Poisson distribution and the log-pdf of the Gamma prior.