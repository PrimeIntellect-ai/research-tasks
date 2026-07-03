I am a researcher running sequence-binding simulations. I have a Python script (`/home/user/mcmc_regression.py`) that parses a FASTA file (`/home/user/sequences.fasta`), extracts sequence features, and uses Markov Chain Monte Carlo (MCMC) to estimate the posterior distribution of binding weights for each feature. 

However, the script crashes during the initialization phase with a `numpy.linalg.LinAlgError: Singular matrix` error. 

Your tasks are to:
1. Identify the bug causing the singular matrix. The observational data extracted from the FASTA file contains perfectly collinear features. 
2. Reshape the observational data in the script to resolve the singularity by removing the redundant feature (`Length`). The model should only use the counts of 'A', 'C', 'G', and 'T' as features.
3. Run the MCMC sampler to estimate the posterior means for the remaining features.
4. Compare these estimated posterior means against a reference dataset provided in `/home/user/reference_weights.csv`. 
5. Calculate the absolute difference between the estimated posterior mean and the reference weight for each of the 4 nucleotide features.
6. Create a log file at `/home/user/results.log` with the exact following format, listing the features and their absolute differences rounded to 2 decimal places:

```
Feature,AbsDiff
A,<value>
C,<value>
G,<value>
T,<value>
```

Do not use any external MCMC libraries like PyMC; the script contains a custom Metropolis-Hastings implementation. Ensure your final results are in the exact format requested.