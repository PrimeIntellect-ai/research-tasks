You are a bioinformatics analyst analyzing sequence data. You need to estimate the posterior distribution of the GC content of a specific gene using Markov Chain Monte Carlo (MCMC).

There is a FASTA file located at `/home/user/sequences.fasta`.

Your task is to:
1. Parse `/home/user/sequences.fasta` and extract the sequence for the record named `target_gene`.
2. Calculate the length of this sequence ($n$) and the total number of G and C bases ($k$).
3. Write a Python script `/home/user/mcmc.py` that implements a Metropolis-Hastings MCMC sampler to estimate the posterior distribution of the GC probability ($\theta$). 
   - **Prior:** $\theta \sim \text{Beta}(2, 2)$.
   - **Likelihood:** $k \sim \text{Binomial}(n, \theta)$.
   - The unnormalized log-posterior is thus proportional to $(k + 1)\log(\theta) + (n - k + 1)\log(1 - \theta)$.
   - **Proposal distribution:** Normal distribution centered at the current $\theta$ with standard deviation $\sigma = 0.05$.
   - **Initialization:** Start the chain at $\theta_0 = 0.5$.
   - **Iterations:** Run the MCMC for exactly 10,000 steps.
   - **Burn-in:** Discard the first 1,000 samples.
   - Set the random seed to `42` using `numpy.random.seed(42)` at the beginning of your script to ensure reproducibility. Use `numpy.random.normal` for proposals and `numpy.random.rand` for acceptance probabilities.
4. Run your script to calculate the mean of the remaining 9,000 samples.
5. Save this mean value, rounded to 3 decimal places, to a file named `/home/user/mcmc_gc_mean.txt`.