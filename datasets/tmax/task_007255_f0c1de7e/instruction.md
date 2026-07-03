You are a bioinformatics analyst tasked with evaluating a set of newly sequenced viral samples against a reference genome. You need to identify the mutation counts, perform Bayesian estimation of the mutation rate, and design a universal diagnostic primer.

Your environment is an Ubuntu Linux system. You must write and run Python code to accomplish this task. 

Here are the requirements:

1. **Environment Setup:** 
   Create a Python virtual environment at `/home/user/bio_env`. Install any standard scientific libraries you need (e.g., `numpy`, `scipy`, `biopython`) into this environment.

2. **Sequence Comparison:**
   You have a reference genome located at `/home/user/reference.fasta` and a set of sample sequences at `/home/user/samples.fasta`. 
   Assume all sample sequences are the same length as the reference and pre-aligned (i.e., no indels, just substitutions).
   Calculate the number of mismatches (Hamming distance) between each sample and the reference.

3. **MCMC Sampling & Posterior Estimation:**
   Model the number of mismatches $x_i$ for each sample as being drawn from a Poisson distribution with an unknown mutation rate $\lambda$:
   $x_i \sim \text{Poisson}(\lambda)$
   
   Assume a Gamma prior for $\lambda$ with shape parameter $\alpha = 2$ and rate parameter $\beta = 1$:
   $P(\lambda) \propto \lambda^{\alpha-1} e^{-\beta\lambda}$
   
   Implement a Metropolis-Hastings Markov Chain Monte Carlo (MCMC) sampler from scratch (or using standard libraries like `scipy.stats`) in Python to draw at least 50,000 samples from the posterior distribution of $\lambda$. Compute the mean of these posterior samples.

4. **Primer Design:**
   Find the longest perfectly conserved contiguous DNA sequence (no mismatches) that is present in the exact same position across the reference AND all sample sequences. If there are multiple conserved regions of the same maximum length, select the one closest to the 5' end (index 0). 

5. **Output Generation:**
   Create a JSON file at `/home/user/analysis_result.json` with the following structure:
   ```json
   {
       "mismatch_counts": [count1, count2, ...],
       "mcmc_posterior_mean": 0.0,
       "conserved_primer": "ACGT..."
   }
   ```
   - `mismatch_counts`: A list of integers representing the number of mismatches for each sequence in the order they appear in `samples.fasta`.
   - `mcmc_posterior_mean`: The mean of your MCMC posterior samples, rounded to exactly 1 decimal place.
   - `conserved_primer`: The longest perfectly conserved nucleotide string.

Complete the analysis and ensure the JSON file is correctly written.