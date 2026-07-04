You are acting as a data scientist for a structural biology lab. We have a protein structure file located at `/home/user/protein.pdb`. 

Your task is to estimate the posterior distribution of the temperature factors (B-factors) of the Alpha-Carbon (CA) atoms in this structure.

Please perform the following steps:
1. Parse the `/home/user/protein.pdb` file and extract the B-factor values (columns 61-66) strictly for atoms where the atom name is exactly `CA` (Alpha-Carbon). 
2. We assume these B-factors are independent and identically distributed, drawn from a Normal distribution $N(\mu, \sigma^2)$.
3. Write a custom script in any language of your choice (using only standard libraries) to perform Markov Chain Monte Carlo (MCMC) sampling using the Metropolis-Hastings algorithm to estimate the posterior distributions of $\mu$ and $\sigma$.
4. Use the following MCMC parameters:
   - Likelihood: Normal distribution
   - Priors: Uniform distribution for $\mu \in [0, 100]$ and Uniform distribution for $\sigma \in [0.1, 30]$.
   - Iterations: 20,000 total steps.
   - Burn-in: Discard the first 5,000 steps.
5. After running the MCMC, calculate the expected value (mean of the posterior samples) for $\mu$ and $\sigma$.
6. Save your final estimations to `/home/user/posterior_stats.txt`. The file must contain exactly two lines with the values rounded to exactly one decimal place, formatted as follows:
```
mu: 40.2
sigma: 5.1
```

You may use any standard programming language (like Python, Perl, AWK, etc.) to write your parsing and MCMC script, but you must only use standard built-in libraries (e.g., you cannot `pip install pymc3` or `scipy`).