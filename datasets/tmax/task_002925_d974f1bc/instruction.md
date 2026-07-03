You are a performance engineer tasked with debugging and optimizing a bioinformatics script.

We have a Python script located at `/home/user/mcmc_mutations.py` that processes a FASTA file (`/home/user/data.fasta`), calculates pairwise Hamming distances between the sequences, and runs a Metropolis-Hastings MCMC sampler to estimate the posterior distribution of a global mutation rate parameter ($\mu$). 

However, the script has two major issues:
1. **Performance Bottleneck:** One of the functions is extremely slow because it relies on nested pure Python loops to perform multi-dimensional array manipulation. 
2. **Numerical Instability:** The `likelihood` function calculates the joint probability by directly multiplying the probabilities of independent events. Because there are many sequence pairs, this quickly underflows to exactly `0.0`, ruining the MCMC sampling (the acceptance ratio becomes invalid or NaN).

Your tasks are as follows:
1. Profile the script to identify the performance bottleneck. Write the exact name of the Python function that takes the vast majority of the execution time to `/home/user/bottleneck.txt`.
2. Optimize that bottleneck function using NumPy vectorization so that it runs significantly faster.
3. Fix the numerical underflow issue by implementing and utilizing a **log-likelihood** function instead of the raw likelihood. Ensure you update the MCMC acceptance ratio logic to correctly use log-probabilities. (Do not change the random seed, prior bounds, proposal distribution, or number of iterations).
4. Run your corrected, optimized script. Save the final posterior mean of $\mu$ (the mean of the `samples` list returned by `run_mcmc`) to `/home/user/posterior_mean.txt`, rounded to 4 decimal places.

Ensure the final optimized script is runnable and produces mathematically correct MCMC samples without underflowing.