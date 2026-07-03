You are a bioinformatics analyst tasked with analyzing DNA sequences. Your team has developed a custom C++ tool called `seq_analyzer` that performs two primary tasks on DNA sequences:
1. **Spectral Analysis (Fourier Transform):** It converts the DNA sequence into a numeric signal (A/T = 0, G/C = 1) and computes the Discrete Fourier Transform (DFT) to find the dominant structural periodicity (ignoring the DC component).
2. **MCMC Posterior Estimation:** It uses a Metropolis-Hastings Markov Chain Monte Carlo (MCMC) sampler to estimate the posterior mean of the GC-content probability based on the sequence data, assuming a Uniform(0,1) prior and a Binomial likelihood.

However, the tool is currently failing its regression tests due to two algorithmic bugs introduced in the latest commit. 

Your task is to:
1. Navigate to `/home/user/seq_analyzer`.
2. Inspect `analyzer.cpp` and fix the two logical bugs:
   - **Bug 1 (Spectral):** The dominant period calculation from the DFT is incorrect. For a sequence of length `N` and the peak frequency index `k` (where `k > 0`), the physical period should be `N / k`. The code currently returns the wrong value.
   - **Bug 2 (MCMC):** The Metropolis-Hastings acceptance ratio is inverted, causing the sampler to move away from the high-probability regions instead of towards them.
3. Compile the software using the provided `Makefile` (run `make`).
4. Run the regression test suite by executing `./run_tests.sh`. Ensure it passes (outputs "Tests passed!").
5. Once fixed and tested, run the tool on the newly sequenced data located at `/home/user/data/reads.fasta`.
6. Save the standard output of the tool when run on `reads.fasta` to exactly `/home/user/results/analysis.log`.

The final `/home/user/results/analysis.log` must have the exact format produced by the corrected program, looking like:
```
Sequence: seq1
Dominant Period: <integer>
GC Posterior Mean: <float>
...
```
(where `<float>` is rounded to 2 decimal places as handled by the C++ code).