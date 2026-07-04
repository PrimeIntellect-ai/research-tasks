You are a bioinformatics analyst tasked with estimating a mutation rate parameter from observational data and protein sequences.

You have been provided with two files:
1. `/home/user/sequences.fasta`: A FASTA file containing several protein sequences.
2. `/home/user/observations.csv`: A CSV file containing observational records of mutations over time for these sequences. The columns are `seq_id`, `time`, and `mutations`.

Your goal is to estimate a global mutation rate parameter, $\lambda$, which scales the expected number of mutations based on the number of Alanine ('A') residues in a sequence.

Perform the following steps:
1. **Bioinformatics Format Parsing:** Read the FASTA file and count the number of Alanine ('A') residues for each sequence. Let this be $X_i$ for sequence $i$.
2. **Observational Data Reshaping:** Read the CSV file and aggregate the data to find the *total* number of mutations for each sequence across all time points. Let this be $Y_i$ for sequence $i$.
3. **MCMC Sampling and Posterior Estimation:** We model the total mutations $Y_i$ as following a Poisson distribution: $Y_i \sim \text{Poisson}(\lambda \cdot X_i)$. 
   Write a Python script to estimate the posterior distribution of $\lambda$ using a Metropolis-Hastings MCMC sampler from scratch (using only `numpy`/`scipy`, no `pymc`).
   
   Use the following MCMC parameters to ensure reproducible results:
   - **Prior:** $\lambda \sim \text{Uniform}(0, 10)$
   - **Initial value:** $\lambda_0 = 1.0$
   - **Proposal distribution:** Normal distribution centered at the current $\lambda$ with a standard deviation of $0.5$. (If the proposed $\lambda$ falls outside the prior bounds, it should be rejected).
   - **Total iterations:** 50,000
   - **Burn-in:** 10,000 (discard the first 10,000 iterations before calculating statistics)
   - **Random Seed:** Set `numpy.random.seed(42)` right before starting the MCMC loop. When generating random numbers in the loop, use `np.random.normal()` for the proposal and `np.random.rand()` for the acceptance threshold.

4. **Output:** Calculate the mean and standard deviation of the remaining 40,000 samples. Save these values in a JSON file at `/home/user/posterior_stats.json` with the keys `"mean"` and `"std"`. Round the values to 3 decimal places.

Ensure the final JSON file is properly formatted.