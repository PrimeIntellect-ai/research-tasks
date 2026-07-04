You are an analyst tasked with estimating the posterior mean of a mutation rate parameter for a set of viral sequences. We have an in-house Python package, `bio_mcmc`, that performs Markov Chain Monte Carlo (MCMC) sampling for sequence alignment and parameter estimation. 

Unfortunately, our nightly regression tests have been failing. The MCMC sampler yields slightly different posterior mean estimates across runs, even when the random seed is strictly fixed. The numerical instability is suspected to be caused by a floating-point reduction order issue during the concurrent log-likelihood computation.

Your tasks are to:
1. Identify and fix the floating-point reduction order bug within the vendored `bio_mcmc` package located at `/app/bio_mcmc-1.2.3`. Ensure the log-likelihood accumulation is mathematically deterministic and doesn't suffer from race conditions or variable ordering due to thread completion.
2. Reinstall the modified package in your environment.
3. Write a Python script `/home/user/run_estimation.py` that:
   - Parses the FASTA file located at `/app/data/viral_sequences.fasta`.
   - Initializes the MCMC sampler using the extracted sequence strings:
     ```python
     import bio_mcmc
     sampler = bio_mcmc.Sampler(sequences, seed=42)
     ```
   - Runs the sampler for exactly `10000` iterations: `samples = sampler.run(10000)`.
   - Calculates the posterior mean of the samples (discarding the first 2000 as burn-in).
   - Writes *only* the final posterior mean (as a float) to `/home/user/posterior_mean.txt`.

Ensure your fix resolves the non-reproducibility. Your final posterior mean must be highly accurate and match our deterministic regression target.